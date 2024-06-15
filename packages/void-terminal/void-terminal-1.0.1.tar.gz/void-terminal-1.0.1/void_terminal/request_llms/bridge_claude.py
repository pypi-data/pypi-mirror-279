# Referenced from https://github.com/GaiZhenbiao/ChuanhuChatGPT 项目

"""
    There are mainly 2 functions in this file

    Functions without multi-threading capability：
    1. predict: Used in normal conversation，Fully interactive，Not multi-threaded

    Functions with multi-threading capability
    2. predict_no_ui_long_connection：Support multi-threading
"""
import logging
import os
import time
import traceback
import json
import requests
from void_terminal.toolbox import get_conf, update_ui, trimmed_format_exc, encode_image, every_image_file_in_path, log_chat
picture_system_prompt = "\nWhen Responding with an Image,Must specify which image is being replied to。All images are provided only in the last question,Even if they are mentioned in the history。请Use'This is Batch NumberX张图像:'的Format来指明您正In描述的是哪张图像。"
Claude_3_Models = ["claude-3-haiku-20240307", "claude-3-sonnet-20240229", "claude-3-opus-20240229"]

# Put your own secrets such as API and proxy address in config_private.py
# When reading, first check if there is a private config_private configuration file（Not controlled by git），If there is，Then overwrite the original config file
from void_terminal.toolbox import get_conf, update_ui, trimmed_format_exc, ProxyNetworkActivate
proxies, TIMEOUT_SECONDS, MAX_RETRY, ANTHROPIC_API_KEY = \
    get_conf('proxies', 'TIMEOUT_SECONDS', 'MAX_RETRY', 'ANTHROPIC_API_KEY')

timeout_bot_msg = '[Local Message] Request timeout. Network error. Please check proxy settings in config.py.' + \
                  'Network error，Check if the proxy server is available，And if the format of the proxy settings is correct，The format must be[Protocol]://[Address]:[Port]，All parts are necessary。'

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
    # Read some information in advance（Used to judge exceptions）
    chunk_decoded = chunk.decode()
    chunkjson = None
    is_last_chunk = False
    need_to_pass = False
    if chunk_decoded.startswith('data:'):
        try:
            chunkjson = json.loads(chunk_decoded[6:])
        except:
            need_to_pass = True
            pass
    elif chunk_decoded.startswith('event:'):
        try:
            event_type = chunk_decoded.split(':')[1].strip()
            if event_type == 'content_block_stop' or event_type == 'message_stop':
                is_last_chunk = True
            elif event_type == 'content_block_start' or event_type == 'message_start':
                need_to_pass = True
                pass
        except:
            need_to_pass = True
            pass
    else:
        need_to_pass = True
        pass
    return need_to_pass, chunkjson, is_last_chunk


def predict_no_ui_long_connection(inputs, llm_kwargs, history=[], sys_prompt="", observe_window=None, console_slience=False):
    """
    Send to chatGPT，Waiting for reply，Completed in one go，Do not display intermediate processes。But internally use the stream method to avoid the network being cut off midway。
    inputs：
        This is the input of this inquiry
    sys_prompt:
        System silent prompt
    llm_kwargs：
        Internal tuning parameters of chatGPT
    history：
        history is the list of previous conversations
    observe_window = None：
        Used to transfer the already output part across threads，Most of the time it`s just for fancy visual effects，Leave it blank。observe_window[0]：Observation window。observe_window[1]：Watchdog
    """
    watch_dog_patience = 5 # The patience of the watchdog, Set 5 seconds
    if len(ANTHROPIC_API_KEY) == 0:
        raise RuntimeError("ANTHROPIC_API_KEY option is not set")
    if inputs == "":     inputs = "Empty input field"
    headers, message = generate_payload(inputs, llm_kwargs, history, sys_prompt, image_paths=None)
    retry = 0


    while True:
        try:
            # make a POST request to the API endpoint, stream=False
            from void_terminal.request_llms.bridge_all import model_info
            endpoint = model_info[llm_kwargs['llm_model']]['endpoint']
            response = requests.post(endpoint, headers=headers, json=message,
                                     proxies=proxies, stream=True, timeout=TIMEOUT_SECONDS);break
        except requests.exceptions.ReadTimeout as e:
            retry += 1
            traceback.print_exc()
            if retry > MAX_RETRY: raise TimeoutError
            if MAX_RETRY!=0: print(f'Request timed out，Retrying ({retry}/{MAX_RETRY}) ……')
    stream_response = response.iter_lines()
    result = ''
    while True:
        try: chunk = next(stream_response)
        except StopIteration:
            break
        except requests.exceptions.ConnectionError:
            chunk = next(stream_response) # Failed，Retry once？If it fails again, there is no way。
        need_to_pass, chunkjson, is_last_chunk = decode_chunk(chunk)
        if chunk:
            try:
                if need_to_pass:
                    pass
                elif is_last_chunk:
                    # logging.info(f'[response] {result}')
                    break
                else:
                    if chunkjson and chunkjson['type'] == 'content_block_delta':
                        result += chunkjson['delta']['text']
                        print(chunkjson['delta']['text'], end='')
                        if observe_window is not None:
                            # Observation window，Display the data already obtained
                            if len(observe_window) >= 1:
                                observe_window[0] += chunkjson['delta']['text']
                            # Watchdog，If the dog is not fed beyond the deadline，then terminate
                            if len(observe_window) >= 2:
                                if (time.time()-observe_window[1]) > watch_dog_patience:
                                    raise RuntimeError("User canceled the program。")
            except Exception as e:
                chunk = get_full_error(chunk, stream_response)
                chunk_decoded = chunk.decode()
                error_msg = chunk_decoded
                print(error_msg)
                raise RuntimeError("Json parsing is not normal")

    return result

def make_media_input(history,inputs,image_paths):
    for image_path in image_paths:
        inputs = inputs + f'<br/><br/><div align="center"><img src="file={os.path.abspath(image_path)}"></div>'
    return inputs

def predict(inputs, llm_kwargs, plugin_kwargs, chatbot, history=[], system_prompt='', stream = True, additional_fn=None):
    """
    Send to chatGPT，Get output in a streaming way。
    Used for basic conversation functions。
    inputs are the inputs for this inquiry
    top_p, Temperature is an internal tuning parameter of chatGPT
    history is the list of previous conversations（Note that both inputs and history，An error of token overflow will be triggered if the content is too long）
    chatbot is the conversation list displayed in WebUI，Modify it，Then yield it out，You can directly modify the conversation interface content
    additional_fn represents which button is clicked，See functional.py for buttons
    """
    if inputs == "":     inputs = "Empty input field"
    if len(ANTHROPIC_API_KEY) == 0:
        chatbot.append((inputs, "ANTHROPIC_API_KEY is not set"))
        yield from update_ui(chatbot=chatbot, history=history, msg="Waiting for response") # Refresh the page
        return

    if additional_fn is not None:
        from void_terminal.core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)

    have_recent_file, image_paths = every_image_file_in_path(chatbot)
    if len(image_paths) > 20:
        chatbot.append((inputs, "Number of Images Exceeds API Limit(20 Sheets)"))
        yield from update_ui(chatbot=chatbot, history=history, msg="Waiting for response")
        return

    if any([llm_kwargs['llm_model'] == model for model in Claude_3_Models]) and have_recent_file:
        if inputs == "" or inputs == "Empty input field":     inputs = "Please describe the given image"
        system_prompt += picture_system_prompt  # Since there is no separate parameter to save the history with images，So can only locate the image by the prompt
        chatbot.append((make_media_input(history,inputs, image_paths), ""))
        yield from update_ui(chatbot=chatbot, history=history, msg="Waiting for response") # Refresh the page
    else:
        chatbot.append((inputs, ""))
        yield from update_ui(chatbot=chatbot, history=history, msg="Waiting for response") # Refresh the page

    try:
        headers, message = generate_payload(inputs, llm_kwargs, history, system_prompt, image_paths)
    except RuntimeError as e:
        chatbot[-1] = (inputs, f"The api-key you provided does not meet the requirements，Does not contain any that can be used for{llm_kwargs['llm_model']}api-key。You may have selected the wrong model or request source。")
        yield from update_ui(chatbot=chatbot, history=history, msg="API key does not meet requirements") # Refresh the page
        return

    history.append(inputs); history.append("")

    retry = 0
    while True:
        try:
            # make a POST request to the API endpoint, stream=True
            from void_terminal.request_llms.bridge_all import model_info
            endpoint = model_info[llm_kwargs['llm_model']]['endpoint']
            response = requests.post(endpoint, headers=headers, json=message,
                                     proxies=proxies, stream=True, timeout=TIMEOUT_SECONDS);break
        except requests.exceptions.ReadTimeout as e:
            retry += 1
            traceback.print_exc()
            if retry > MAX_RETRY: raise TimeoutError
            if MAX_RETRY!=0: print(f'Request timed out，Retrying ({retry}/{MAX_RETRY}) ……')
    stream_response = response.iter_lines()
    gpt_replying_buffer = ""

    while True:
        try: chunk = next(stream_response)
        except StopIteration:
            break
        except requests.exceptions.ConnectionError:
            chunk = next(stream_response) # Failed，Retry once？If it fails again, there is no way。
        need_to_pass, chunkjson, is_last_chunk = decode_chunk(chunk)
        if chunk:
            try:
                if need_to_pass:
                    pass
                elif is_last_chunk:
                    log_chat(llm_model=llm_kwargs["llm_model"], input_str=inputs, output_str=gpt_replying_buffer)
                    # logging.info(f'[response] {gpt_replying_buffer}')
                    break
                else:
                    if chunkjson and chunkjson['type'] == 'content_block_delta':
                        gpt_replying_buffer += chunkjson['delta']['text']
                        history[-1] = gpt_replying_buffer
                        chatbot[-1] = (history[-2], history[-1])
                        yield from update_ui(chatbot=chatbot, history=history, msg='Normal') # Refresh the page

            except Exception as e:
                chunk = get_full_error(chunk, stream_response)
                chunk_decoded = chunk.decode()
                error_msg = chunk_decoded
                print(error_msg)
                raise RuntimeError("Json parsing is not normal")

def multiple_picture_types(image_paths):
    """
    Return image/jpeg based on image type, image/png, image/gif, image/webp，Return image/jpeg If Unable to Determine
    """
    for image_path in image_paths:
        if image_path.endswith('.jpeg') or image_path.endswith('.jpg'):
            return 'image/jpeg'
        elif image_path.endswith('.png'):
            return 'image/png'
        elif image_path.endswith('.gif'):
            return 'image/gif'
        elif image_path.endswith('.webp'):
            return 'image/webp'
    return 'image/jpeg'

def generate_payload(inputs, llm_kwargs, history, system_prompt, image_paths):
    """
    Integrate all information，Select LLM model，Generate http request，Prepare to send request
    """

    conversation_cnt = len(history) // 2

    messages = []

    if conversation_cnt:
        for index in range(0, 2*conversation_cnt, 2):
            what_i_have_asked = {}
            what_i_have_asked["role"] = "user"
            what_i_have_asked["content"] = [{"type": "text", "text": history[index]}]
            what_gpt_answer = {}
            what_gpt_answer["role"] = "assistant"
            what_gpt_answer["content"] = [{"type": "text", "text": history[index+1]}]
            if what_i_have_asked["content"][0]["text"] != "":
                if what_i_have_asked["content"][0]["text"] == "": continue
                if what_i_have_asked["content"][0]["text"] == timeout_bot_msg: continue
                messages.append(what_i_have_asked)
                messages.append(what_gpt_answer)
            else:
                messages[-1]['content'][0]['text'] = what_gpt_answer['content'][0]['text']

    if any([llm_kwargs['llm_model'] == model for model in Claude_3_Models]) and image_paths:
        what_i_ask_now = {}
        what_i_ask_now["role"] = "user"
        what_i_ask_now["content"] = []
        for image_path in image_paths:
            what_i_ask_now["content"].append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": multiple_picture_types(image_paths),
                    "data": encode_image(image_path),
                }
            })
        what_i_ask_now["content"].append({"type": "text", "text": inputs})
    else:
        what_i_ask_now = {}
        what_i_ask_now["role"] = "user"
        what_i_ask_now["content"] = [{"type": "text", "text": inputs}]
    messages.append(what_i_ask_now)
    # Start Organizing Headers and Messages
    headers = {
        'x-api-key': ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json'
    }
    payload = {
        'model': llm_kwargs['llm_model'],
        'max_tokens': 4096,
        'messages': messages,
        'temperature': llm_kwargs['temperature'],
        'stream': True,
        'system': system_prompt
    }
    return headers, payload
