# Referenced from https://github.com/GaiZhenbiao/ChuanhuChatGPT 项目

"""
    This file mainly contains three functions

    Functions without multi-threading capability：
    1. predict: Used in normal conversation，Fully interactive，Not multi-threaded

    Functions with multi-threading capability
    2. predict_no_ui_long_connection：Support multi-threading
"""

import json
import time
import fake_gradio as gr
import logging
import traceback
import requests
import importlib
import random

# Put your own secrets such as API and proxy address in config_private.py
# When reading, first check if there is a private config_private configuration file（Not controlled by git），If there is，Then overwrite the original config file
from void_terminal.toolbox import get_conf, update_ui, is_any_api_key, select_api_key, what_keys, clip_history
from void_terminal.toolbox import trimmed_format_exc, is_the_upload_folder, read_one_api_model_name, log_chat
from void_terminal.toolbox import ChatBotWithCookies
proxies, TIMEOUT_SECONDS, MAX_RETRY, API_ORG, AZURE_CFG_ARRAY = \
    get_conf('proxies', 'TIMEOUT_SECONDS', 'MAX_RETRY', 'API_ORG', 'AZURE_CFG_ARRAY')

timeout_bot_msg = '[Local Message] Request timeout. Network error. Please check proxy settings in config.py.' + \
                  'Network error，Check if the proxy server is available，And if the format of the proxy settings is correct，The format must be[Protocol]://[Address]:[Port]，All parts are necessary。'

def get_full_error(chunk, stream_response):
    """
        Get the complete error message returned from Cohere
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
        chunkjson = json.loads(chunk_decoded)
        has_choices = 'choices' in chunkjson
        if has_choices: choice_valid = (len(chunkjson['choices']) > 0)
        if has_choices and choice_valid: has_content = ("content" in chunkjson['choices'][0]["delta"])
        if has_content: has_content = (chunkjson['choices'][0]["delta"]["content"] is not None)
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
    if "The API name you wrote yourself" in endpoint:
        raise ValueError("Endpoint is incorrect, Please check the configuration of AZURE_ENDPOINT! The current Endpoint is:" + endpoint)
    return endpoint

def predict_no_ui_long_connection(inputs:str, llm_kwargs:dict, history:list=[], sys_prompt:str="", observe_window:list=None, console_slience:bool=False):
    """
    Send，Waiting for reply，Completed in one go，Do not display intermediate processes。But internally use the stream method to avoid the network being cut off midway。
    inputs：
        This is the input of this inquiry
    sys_prompt:
        System silent prompt
    llm_kwargs：
        Internal tuning parameters
    history：
        history is the list of previous conversations
    observe_window = None：
        Used to transfer the already output part across threads，Most of the time it`s just for fancy visual effects，Leave it blank。observe_window[0]：Observation window。observe_window[1]：Watchdog
    """
    watch_dog_patience = 5 # The patience of the watchdog, Set 5 seconds
    headers, payload = generate_payload(inputs, llm_kwargs, history, system_prompt=sys_prompt, stream=True)
    retry = 0
    while True:
        try:
            # make a POST request to the API endpoint, stream=False
            from void_terminal.request_llms.bridge_all import model_info
            endpoint = verify_endpoint(model_info[llm_kwargs['llm_model']]['endpoint'])
            response = requests.post(endpoint, headers=headers, proxies=proxies,
                                    json=payload, stream=True, timeout=TIMEOUT_SECONDS); break
        except requests.exceptions.ReadTimeout as e:
            retry += 1
            traceback.print_exc()
            if retry > MAX_RETRY: raise TimeoutError
            if MAX_RETRY!=0: print(f'Request timed out，Retrying ({retry}/{MAX_RETRY}) ……')

    stream_response = response.iter_lines()
    result = ''
    json_data = None
    while True:
        try: chunk = next(stream_response)
        except StopIteration:
            break
        except requests.exceptions.ConnectionError:
            chunk = next(stream_response) # Failed，Retry once？If it fails again, there is no way。
        chunk_decoded, chunkjson, has_choices, choice_valid, has_content, has_role = decode_chunk(chunk)
        if chunkjson['event_type'] == 'stream-start': continue
        if chunkjson['event_type'] == 'text-generation':
            result += chunkjson["text"]
            if not console_slience: print(chunkjson["text"], end='')
            if observe_window is not None:
                # Observation window，Display the data already obtained
                if len(observe_window) >= 1:
                    observe_window[0] += chunkjson["text"]
                # Watchdog，If the dog is not fed beyond the deadline，then terminate
                if len(observe_window) >= 2:
                    if (time.time()-observe_window[1]) > watch_dog_patience:
                        raise RuntimeError("User canceled the program。")
        if chunkjson['event_type'] == 'stream-end': break
    return result


def predict(inputs:str, llm_kwargs:dict, plugin_kwargs:dict, chatbot:ChatBotWithCookies,
            history:list=[], system_prompt:str='', stream:bool=True, additional_fn:str=None):
    """
    Send to chatGPT，Get output in a streaming way。
    Used for basic conversation functions。
    inputs are the inputs for this inquiry
    top_p, Temperature is an internal tuning parameter of chatGPT
    history is the list of previous conversations（Note that both inputs and history，An error of token overflow will be triggered if the content is too long）
    chatbot is the conversation list displayed in WebUI，Modify it，Then yield it out，You can directly modify the conversation interface content
    additional_fn represents which button is clicked，See functional.py for buttons
    """
    # if is_any_api_key(inputs):
    #     chatbot._cookies['api_key'] = inputs
    #     chatbot.append(("Input已识别为Cohere的api_key", what_keys(inputs)))
    #     yield from update_ui(chatbot=chatbot, history=history, msg="api_key has been imported") # Refresh the page
    #     return
    # elif not is_any_api_key(chatbot._cookies['api_key']):
    #     chatbot.append((inputs, "Missing api_key。\n\n1. Temporary solution：Enter the api_key Directly in the Input Area，Submit after pressing Enter。2. Long-term Solution：Configure in config.py。"))
    #     yield from update_ui(chatbot=chatbot, history=history, msg="Missing api_key") # Refresh the page
    #     return

    user_input = inputs
    if additional_fn is not None:
        from void_terminal.core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)

    raw_input = inputs
    # logging.info(f'[raw_input] {raw_input}')
    chatbot.append((inputs, ""))
    yield from update_ui(chatbot=chatbot, history=history, msg="Waiting for response") # Refresh the page

    # check mis-behavior
    if is_the_upload_folder(user_input):
        chatbot[-1] = (inputs, f"[Local Message] Operation error detected! After you upload the document，Click the `**Function Plugin Area**` button for processing，Do not click the `Submit` button or the `Basic Function Area` button。")
        yield from update_ui(chatbot=chatbot, history=history, msg="Normal") # Refresh the page
        time.sleep(2)

    try:
        headers, payload = generate_payload(inputs, llm_kwargs, history, system_prompt, stream)
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

    history.append(inputs); history.append("")

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
                # Such errors occur in non-Cohere official interfaces，Cohere and API2D will not go here
                chunk_decoded = chunk.decode()
                error_msg = chunk_decoded
                # Other situations，Direct return error
                chatbot, history = handle_error(inputs, llm_kwargs, chatbot, history, chunk_decoded, error_msg)
                yield from update_ui(chatbot=chatbot, history=history, msg="Non-Cohere Official Interface Returned an Error:" + chunk.decode()) # Refresh the page
                return

            # Read some information in advance （Used to judge exceptions）
            chunk_decoded, chunkjson, has_choices, choice_valid, has_content, has_role = decode_chunk(chunk)

            if chunkjson:
                try:
                    if chunkjson['event_type'] == 'stream-start':
                        continue
                    if chunkjson['event_type'] == 'text-generation':
                        gpt_replying_buffer = gpt_replying_buffer + chunkjson["text"]
                        history[-1] = gpt_replying_buffer
                        chatbot[-1] = (history[-2], history[-1])
                        yield from update_ui(chatbot=chatbot, history=history, msg="Normal") # Refresh the page
                    if chunkjson['event_type'] == 'stream-end':
                        log_chat(llm_model=llm_kwargs["llm_model"], input_str=inputs, output_str=gpt_replying_buffer)
                        history[-1] = gpt_replying_buffer
                        chatbot[-1] = (history[-2], history[-1])
                        yield from update_ui(chatbot=chatbot, history=history, msg="Normal") # Refresh the page
                        break
                except Exception as e:
                    yield from update_ui(chatbot=chatbot, history=history, msg="Json parsing is not normal") # Refresh the page
                    chunk = get_full_error(chunk, stream_response)
                    chunk_decoded = chunk.decode()
                    error_msg = chunk_decoded
                    chatbot, history = handle_error(inputs, llm_kwargs, chatbot, history, chunk_decoded, error_msg)
                    yield from update_ui(chatbot=chatbot, history=history, msg="Json exception" + error_msg) # Refresh the page
                    print(error_msg)
                    return

def handle_error(inputs, llm_kwargs, chatbot, history, chunk_decoded, error_msg):
    from void_terminal.request_llms.bridge_all import model_info
    Cohere_website = ' Please log in to Cohere for details https://platform.Cohere.com/signup'
    if "reduce the length" in error_msg:
        if len(history) >= 2: history[-1] = ""; history[-2] = "" # Clear the current overflow input：history[-2] It is the input of this time, history[-1] It is the output of this time
        history = clip_history(inputs=inputs, history=history, tokenizer=model_info[llm_kwargs['llm_model']]['tokenizer'],
                                               max_token_limit=(model_info[llm_kwargs['llm_model']]['max_token'])) # Release at least half of the history
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Reduce the length. The input is too long this time, Or the historical data is too long. Historical cached data has been partially released, You can try again. (If it fails again, it is more likely due to input being too long.)")
    elif "does not exist" in error_msg:
        chatbot[-1] = (chatbot[-1][0], f"[Local Message] Model {llm_kwargs['llm_model']} Model does not exist, Or you do not have the qualification for experience.")
    elif "Incorrect API key" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Incorrect API key. Cohere reports an incorrect API_KEY., Service refused. " + Cohere_website)
    elif "exceeded your current quota" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] You exceeded your current quota. Cohere due to insufficient account quota, Service refused." + Cohere_website)
    elif "account is not active" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Your account is not active. Cohere cites the account`s inactivation as the reason, Service refused." + Cohere_website)
    elif "associated with a deactivated account" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] You are associated with a deactivated account. Cohere due to account deactivation, Service refused." + Cohere_website)
    elif "API key has been deactivated" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] API key has been deactivated. Cohere cited account expiration as the reason, Service refused." + Cohere_website)
    elif "bad forward key" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Bad forward key. API2D account balance is insufficient.")
    elif "Not enough point" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Not enough point. API2D account points are insufficient.")
    else:
        from void_terminal.toolbox import regular_txt_to_markdown
        tb_str = '```\n' + trimmed_format_exc() + '```'
        chatbot[-1] = (chatbot[-1][0], f"[Local Message] Exception \n\n{tb_str} \n\n{regular_txt_to_markdown(chunk_decoded)}")
    return chatbot, history

def generate_payload(inputs, llm_kwargs, history, system_prompt, stream):
    """
    Integrate all information，Select LLM model，Generate http request，Prepare to send request
    """
    # if not is_any_api_key(llm_kwargs['api_key']):
    #     raise AssertionError("You provided an incorrect API_KEY。\n\n1. Temporary solution：Enter the api_key Directly in the Input Area，Submit after pressing Enter。2. Long-term Solution：Configure in config.py。")

    api_key = select_api_key(llm_kwargs['api_key'], llm_kwargs['llm_model'])

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    if API_ORG.startswith('org-'): headers.update({"Cohere-Organization": API_ORG})
    if llm_kwargs['llm_model'].startswith('azure-'):
        headers.update({"api-key": api_key})
        if llm_kwargs['llm_model'] in AZURE_CFG_ARRAY.keys():
            azure_api_key_unshared = AZURE_CFG_ARRAY[llm_kwargs['llm_model']]["AZURE_API_KEY"]
            headers.update({"api-key": azure_api_key_unshared})

    conversation_cnt = len(history) // 2

    messages = [{"role": "SYSTEM", "message": system_prompt}]
    if conversation_cnt:
        for index in range(0, 2*conversation_cnt, 2):
            what_i_have_asked = {}
            what_i_have_asked["role"] = "USER"
            what_i_have_asked["message"] = history[index]
            what_gpt_answer = {}
            what_gpt_answer["role"] = "CHATBOT"
            what_gpt_answer["message"] = history[index+1]
            if what_i_have_asked["message"] != "":
                if what_gpt_answer["message"] == "": continue
                if what_gpt_answer["message"] == timeout_bot_msg: continue
                messages.append(what_i_have_asked)
                messages.append(what_gpt_answer)
            else:
                messages[-1]['message'] = what_gpt_answer['message']

    model = llm_kwargs['llm_model']
    if model.startswith('cohere-'): model = model[len('cohere-'):]
    payload = {
        "model": model,
        "message": inputs,
        "chat_history": messages,
        "temperature": llm_kwargs['temperature'],  # 1.0,
        "top_p": llm_kwargs['top_p'],  # 1.0,
        "n": 1,
        "stream": stream,
        "presence_penalty": 0,
        "frequency_penalty": 0,
    }

    return headers,payload


