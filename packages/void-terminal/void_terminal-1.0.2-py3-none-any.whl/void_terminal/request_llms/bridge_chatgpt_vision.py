"""
    This file mainly contains three functions

    Functions without multi-threading capability：
    1. predict: Used in normal conversation，Fully interactive，Not multi-threaded

    Functions with multi-threading capability
    2. predict_no_ui_long_connection：Support multi-threading
"""

import json
import time
import logging
import requests
import base64
import os
import glob
from void_terminal.toolbox import get_conf, update_ui, is_any_api_key, select_api_key, what_keys, clip_history, trimmed_format_exc, is_the_upload_folder, \
    update_ui_lastest_msg, get_max_token, encode_image, have_any_recent_upload_image_files


proxies, TIMEOUT_SECONDS, MAX_RETRY, API_ORG, AZURE_CFG_ARRAY = \
    get_conf('proxies', 'TIMEOUT_SECONDS', 'MAX_RETRY', 'API_ORG', 'AZURE_CFG_ARRAY')

timeout_bot_msg = '[Local Message] Request timeout. Network error. Please check proxy settings in config.py.' + \
                  'Network error，Check if the proxy server is available，And if the format of the proxy settings is correct，The format must be[Protocol]://[Address]:[Port]，All parts are necessary。'


def report_invalid_key(key):
    if get_conf("BLOCK_INVALID_APIKEY"):
        # Experimental feature，Automatically detect and block invalid keys，Please do not use
        from void_terminal.request_llms.key_manager import ApiKeyManager
        api_key = ApiKeyManager().add_key_to_blacklist(key)

def get_full_error(chunk, stream_response):
    """
        Get the complete error message returned from OpenAI
    """
    while True:
        try:
            chunk += next(stream_response)
        except:
            break
    return chunk

def decode_chunk(chunk):
    # Read some information in advance （Used to judge exceptions）
    chunk_decoded = chunk.decode()
    chunkjson = None
    has_choices = False
    choice_valid = False
    has_content = False
    has_role = False
    try:
        chunkjson = json.loads(chunk_decoded[6:])
        has_choices = 'choices' in chunkjson
        if has_choices: choice_valid = (len(chunkjson['choices']) > 0)
        if has_choices and choice_valid: has_content = "content" in chunkjson['choices'][0]["delta"]
        if has_choices and choice_valid: has_role = "role" in chunkjson['choices'][0]["delta"]
    except:
        pass
    return chunk_decoded, chunkjson, has_choices, choice_valid, has_content, has_role

from functools import lru_cache
@lru_cache(maxsize=32)
def verify_endpoint(endpoint):
    """
        Check if the endpoint is available
    """
    return endpoint

def predict_no_ui_long_connection(inputs, llm_kwargs, history=[], sys_prompt="", observe_window=None, console_slience=False):
    raise NotImplementedError


def predict(inputs, llm_kwargs, plugin_kwargs, chatbot, history=[], system_prompt='', stream = True, additional_fn=None):

    have_recent_file, image_paths = have_any_recent_upload_image_files(chatbot)

    if is_any_api_key(inputs):
        chatbot._cookies['api_key'] = inputs
        chatbot.append(("The input has been recognized as OpenAI`s api_key", what_keys(inputs)))
        yield from update_ui(chatbot=chatbot, history=history, msg="api_key has been imported") # Refresh the page
        return
    elif not is_any_api_key(chatbot._cookies['api_key']):
        chatbot.append((inputs, "Missing api_key。\n\n1. Temporary solution：Enter the api_key Directly in the Input Area，Submit after pressing Enter。2. Long-term Solution：Configure in config.py。"))
        yield from update_ui(chatbot=chatbot, history=history, msg="Missing api_key") # Refresh the page
        return
    if not have_recent_file:
        chatbot.append((inputs, "No recently uploaded image files detected，Please upload images in jpg format，In addition，Please note that the extension name needs to be lowercase"))
        yield from update_ui(chatbot=chatbot, history=history, msg="Waiting for image") # Refresh the page
        return
    if os.path.exists(inputs):
        chatbot.append((inputs, "The file you uploaded has been received，You don`t need to emphasize the file path again，Please enter your question directly。"))
        yield from update_ui(chatbot=chatbot, history=history, msg="Waiting for instructions") # Refresh the page
        return


    user_input = inputs
    if additional_fn is not None:
        from void_terminal.core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)

    raw_input = inputs
    logging.info(f'[raw_input] {raw_input}')
    def make_media_input(inputs, image_paths):
        for image_path in image_paths:
            inputs = inputs + f'<br/><br/><div align="center"><img src="file={os.path.abspath(image_path)}"></div>'
        return inputs
    chatbot.append((make_media_input(inputs, image_paths), ""))
    yield from update_ui(chatbot=chatbot, history=history, msg="Waiting for response") # Refresh the page

    # check mis-behavior
    if is_the_upload_folder(user_input):
        chatbot[-1] = (inputs, f"[Local Message] Operation error detected! After you upload the document，Click the `**Function Plugin Area**` button for processing，Do not click the `Submit` button or the `Basic Function Area` button。")
        yield from update_ui(chatbot=chatbot, history=history, msg="Normal") # Refresh the page
        time.sleep(2)

    try:
        headers, payload, api_key = generate_payload(inputs, llm_kwargs, history, system_prompt, image_paths)
    except RuntimeError as e:
        chatbot[-1] = (inputs, f"The api-key you provided does not meet the requirements，Does not contain any that can be used for{llm_kwargs['llm_model']}api-key。You may have selected the wrong model or request source。")
        yield from update_ui(chatbot=chatbot, history=history, msg="API key does not meet requirements") # Refresh the page
        return

    # Check if the endpoint is valid
    try:
        from void_terminal.request_llms.bridge_all import model_info
        endpoint = verify_endpoint(model_info[llm_kwargs['llm_model']]['endpoint'])
    except:
        tb_str = '```\n' + trimmed_format_exc() + '```'
        chatbot[-1] = (inputs, tb_str)
        yield from update_ui(chatbot=chatbot, history=history, msg="Endpoint does not meet the requirements") # Refresh the page
        return

    history.append(make_media_input(inputs, image_paths))
    history.append("")

    retry = 0
    while True:
        try:
            # make a POST request to the API endpoint, stream=True
            response = requests.post(endpoint, headers=headers, proxies=proxies,
                                    json=payload, stream=True, timeout=TIMEOUT_SECONDS);break
        except:
            retry += 1
            chatbot[-1] = ((chatbot[-1][0], timeout_bot_msg))
            retry_msg = f"，Retrying ({retry}/{MAX_RETRY}) ……" if MAX_RETRY > 0 else ""
            yield from update_ui(chatbot=chatbot, history=history, msg="Request timed out"+retry_msg) # Refresh the page
            if retry > MAX_RETRY: raise TimeoutError

    gpt_replying_buffer = ""

    is_head_of_the_stream = True
    if stream:
        stream_response =  response.iter_lines()
        while True:
            try:
                chunk = next(stream_response)
            except StopIteration:
                # such errors occur in non-OpenAI official interfaces，OpenAI and API2D will not go here
                chunk_decoded = chunk.decode()
                error_msg = chunk_decoded
                # First exclude a third-party bug where one-api does not have a done data package
                if len(gpt_replying_buffer.strip()) > 0 and len(error_msg) == 0:
                    yield from update_ui(chatbot=chatbot, history=history, msg="Detected defective non-OpenAI official interface，It is recommended to choose a more stable interface。")
                    break
                # Other situations，Direct return error
                chatbot, history = handle_error(inputs, llm_kwargs, chatbot, history, chunk_decoded, error_msg, api_key)
                yield from update_ui(chatbot=chatbot, history=history, msg="Non-OpenAI official interface returned an error:" + chunk.decode()) # Refresh the page
                return

            # Read some information in advance （Used to judge exceptions）
            chunk_decoded, chunkjson, has_choices, choice_valid, has_content, has_role = decode_chunk(chunk)

            if is_head_of_the_stream and (r'"object":"error"' not in chunk_decoded) and (r"content" not in chunk_decoded):
                # The first frame of the data stream does not carry content
                is_head_of_the_stream = False; continue

            if chunk:
                try:
                    if has_choices and not choice_valid:
                        # Some errors caused by garbage third-party interfaces
                        continue
                    # The former is the termination condition of API2D，The latter is the termination condition of OPENAI
                    if ('data: [DONE]' in chunk_decoded) or (len(chunkjson['choices'][0]["delta"]) == 0):
                        # Judged as the end of the data stream，gpt_replying_buffer is also written
                        lastmsg = chatbot[-1][-1] + f"\n\n\n\n「{llm_kwargs['llm_model']}Call ended，TranslatedText，If you have further questions，Please switch models in time。」"
                        yield from update_ui_lastest_msg(lastmsg, chatbot, history, delay=1)
                        logging.info(f'[response] {gpt_replying_buffer}')
                        break
                    # Processing the body of the data stream
                    status_text = f"finish_reason: {chunkjson['choices'][0].get('finish_reason', 'null')}"
                    # If an exception is thrown here，It is usually because the text is too long，See the output of get_full_error for details
                    if has_content:
                        # Normal situation
                        gpt_replying_buffer = gpt_replying_buffer + chunkjson['choices'][0]["delta"]["content"]
                    elif has_role:
                        # Some third-party interfaces encounter such errors，Let`s make it compatible
                        continue
                    else:
                        # Some errors caused by garbage third-party interfaces
                        gpt_replying_buffer = gpt_replying_buffer + chunkjson['choices'][0]["delta"]["content"]

                    history[-1] = gpt_replying_buffer
                    chatbot[-1] = (history[-2], history[-1])
                    yield from update_ui(chatbot=chatbot, history=history, msg=status_text) # Refresh the page
                except Exception as e:
                    yield from update_ui(chatbot=chatbot, history=history, msg="Json parsing is not normal") # Refresh the page
                    chunk = get_full_error(chunk, stream_response)
                    chunk_decoded = chunk.decode()
                    error_msg = chunk_decoded
                    chatbot, history = handle_error(inputs, llm_kwargs, chatbot, history, chunk_decoded, error_msg, api_key)
                    yield from update_ui(chatbot=chatbot, history=history, msg="Json exception" + error_msg) # Refresh the page
                    print(error_msg)
                    return

def handle_error(inputs, llm_kwargs, chatbot, history, chunk_decoded, error_msg, api_key=""):
    from void_terminal.request_llms.bridge_all import model_info
    openai_website = ' Please log in to OpenAI to view details at https://platform.openai.com/signup'
    if "reduce the length" in error_msg:
        if len(history) >= 2: history[-1] = ""; history[-2] = "" # Clear the current overflow input：history[-2] It is the input of this time, history[-1] It is the output of this time
        history = clip_history(inputs=inputs, history=history, tokenizer=model_info[llm_kwargs['llm_model']]['tokenizer'],
                                               max_token_limit=(model_info[llm_kwargs['llm_model']]['max_token'])) # Release at least half of the history
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Reduce the length. The input is too long this time, Or the historical data is too long. Historical cached data has been partially released, You can try again. (If it fails again, it is more likely due to input being too long.)")
    elif "does not exist" in error_msg:
        chatbot[-1] = (chatbot[-1][0], f"[Local Message] Model {llm_kwargs['llm_model']} Model does not exist, Or you do not have the qualification for experience.")
    elif "Incorrect API key" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Incorrect API key. OpenAI claims that an incorrect API_KEY was provided, Service refused. " + openai_website); report_invalid_key(api_key)
    elif "exceeded your current quota" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] You exceeded your current quota. OpenAI claims that the account balance is insufficient, Service refused." + openai_website); report_invalid_key(api_key)
    elif "account is not active" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Your account is not active. OpenAI states that it is due to account expiration, Service refused." + openai_website); report_invalid_key(api_key)
    elif "associated with a deactivated account" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] You are associated with a deactivated account. OpenAI considers it as an account expiration, Service refused." + openai_website); report_invalid_key(api_key)
    elif "API key has been deactivated" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] API key has been deactivated. OpenAI considers it as an account failure, Service refused." + openai_website); report_invalid_key(api_key)
    elif "bad forward key" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Bad forward key. API2D account balance is insufficient.")
    elif "Not enough point" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Not enough point. API2D account points are insufficient.")
    else:
        from void_terminal.toolbox import regular_txt_to_markdown
        tb_str = '```\n' + trimmed_format_exc() + '```'
        chatbot[-1] = (chatbot[-1][0], f"[Local Message] Exception \n\n{tb_str} \n\n{regular_txt_to_markdown(chunk_decoded)}")
    return chatbot, history


def generate_payload(inputs, llm_kwargs, history, system_prompt, image_paths):
    """
    Integrate all information，Select LLM model，Generate http request，Prepare to send request
    """
    if not is_any_api_key(llm_kwargs['api_key']):
        raise AssertionError("You provided an incorrect API_KEY。\n\n1. Temporary solution：Enter the api_key Directly in the Input Area，Submit after pressing Enter。2. Long-term Solution：Configure in config.py。")

    api_key = select_api_key(llm_kwargs['api_key'], llm_kwargs['llm_model'])

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    if API_ORG.startswith('org-'): headers.update({"OpenAI-Organization": API_ORG})
    if llm_kwargs['llm_model'].startswith('azure-'):
        headers.update({"api-key": api_key})
        if llm_kwargs['llm_model'] in AZURE_CFG_ARRAY.keys():
            azure_api_key_unshared = AZURE_CFG_ARRAY[llm_kwargs['llm_model']]["AZURE_API_KEY"]
            headers.update({"api-key": azure_api_key_unshared})

    base64_images = []
    for image_path in image_paths:
        base64_images.append(encode_image(image_path))

    messages = []
    what_i_ask_now = {}
    what_i_ask_now["role"] = "user"
    what_i_ask_now["content"] = []
    what_i_ask_now["content"].append({
        "type": "text",
        "text": inputs
    })

    for image_path, base64_image in zip(image_paths, base64_images):
        what_i_ask_now["content"].append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })

    messages.append(what_i_ask_now)
    model = llm_kwargs['llm_model']
    if llm_kwargs['llm_model'].startswith('api2d-'):
        model = llm_kwargs['llm_model'][len('api2d-'):]

    payload = {
        "model": model,
        "messages": messages,
        "temperature": llm_kwargs['temperature'],   # 1.0,
        "top_p": llm_kwargs['top_p'],               # 1.0,
        "n": 1,
        "stream": True,
        "max_tokens": get_max_token(llm_kwargs),
        "presence_penalty": 0,
        "frequency_penalty": 0,
    }
    try:
        print(f" {llm_kwargs['llm_model']} : {inputs[:100]} ..........")
    except:
        print('There may be garbled characters in the input。')
    return headers, payload, api_key


