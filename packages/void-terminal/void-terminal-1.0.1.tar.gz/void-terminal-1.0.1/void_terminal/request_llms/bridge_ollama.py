# Inspired by bridge_chatgpt.py in the same directory

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
from void_terminal.toolbox import get_conf, update_ui, trimmed_format_exc, is_the_upload_folder, read_one_api_model_name
proxies, TIMEOUT_SECONDS, MAX_RETRY = get_conf(
    "proxies", "TIMEOUT_SECONDS", "MAX_RETRY"
)

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
    try:
        chunkjson = json.loads(chunk_decoded)
        is_last_chunk = chunkjson.get("done", False)
    except:
        pass
    return chunk_decoded, chunkjson, is_last_chunk

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
    if inputs == "":     inputs = "Empty input field"
    headers, payload = generate_payload(inputs, llm_kwargs, history, system_prompt=sys_prompt, stream=True)
    retry = 0
    while True:
        try:
            # make a POST request to the API endpoint, stream=False
            from void_terminal.request_llms.bridge_all import model_info
            endpoint = model_info[llm_kwargs['llm_model']]['endpoint']
            response = requests.post(endpoint, headers=headers, proxies=proxies,
                                    json=payload, stream=True, timeout=TIMEOUT_SECONDS); break
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
        chunk_decoded, chunkjson, is_last_chunk = decode_chunk(chunk)
        if chunk:
            try:
                if is_last_chunk:
                    # Judged as the end of the data stream，gpt_replying_buffer is also written
                    logging.info(f'[response] {result}')
                    break
                result += chunkjson['message']["content"]
                if not console_slience: print(chunkjson['message']["content"], end='')
                if observe_window is not None:
                    # Observation window，Display the data already obtained
                    if len(observe_window) >= 1:
                        observe_window[0] += chunkjson['message']["content"]
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
    user_input = inputs
    if additional_fn is not None:
        from void_terminal.core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)

    raw_input = inputs
    logging.info(f'[raw_input] {raw_input}')
    chatbot.append((inputs, ""))
    yield from update_ui(chatbot=chatbot, history=history, msg="Waiting for response") # Refresh the page

    # check mis-behavior
    if is_the_upload_folder(user_input):
        chatbot[-1] = (inputs, f"[Local Message] Operation error detected! After you upload the document，Click the `**Function Plugin Area**` button for processing，Do not click the `Submit` button or the `Basic Function Area` button。")
        yield from update_ui(chatbot=chatbot, history=history, msg="Normal") # Refresh the page
        time.sleep(2)

    headers, payload = generate_payload(inputs, llm_kwargs, history, system_prompt, stream)

    from void_terminal.request_llms.bridge_all import model_info
    endpoint = model_info[llm_kwargs['llm_model']]['endpoint']

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

    if stream:
        stream_response =  response.iter_lines()
        while True:
            try:
                chunk = next(stream_response)
            except StopIteration:
                break
            except requests.exceptions.ConnectionError:
                chunk = next(stream_response) # Failed，Retry once？If it fails again, there is no way。

            # Read some information in advance （Used to judge exceptions）
            chunk_decoded, chunkjson, is_last_chunk = decode_chunk(chunk)

            if chunk:
                try:
                    if is_last_chunk:
                        # Judged as the end of the data stream，gpt_replying_buffer is also written
                        logging.info(f'[response] {gpt_replying_buffer}')
                        break
                    # Processing the body of the data stream
                    try:
                        status_text = f"finish_reason: {chunkjson['error'].get('message', 'null')}"
                    except:
                        status_text = "finish_reason: null"
                    gpt_replying_buffer = gpt_replying_buffer + chunkjson['message']["content"]
                    # If an exception is thrown here，It is usually because the text is too long，See the output of get_full_error for details
                    history[-1] = gpt_replying_buffer
                    chatbot[-1] = (history[-2], history[-1])
                    yield from update_ui(chatbot=chatbot, history=history, msg=status_text) # Refresh the page
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
    if "bad_request" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Has exceeded the model`s maximum context or there is a model format error,Please try to reduce the amount of text in a single input。")
    elif "authentication_error" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Incorrect API key. Please ensure the API key is valid。")
    elif "not_found" in error_msg:
        chatbot[-1] = (chatbot[-1][0], f"[Local Message] {llm_kwargs['llm_model']} Invalid，Please ensure the use of lowercase model names。")
    elif "rate_limit" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] Encountered control request rate limit，Please try again in one minute。")
    elif "system_busy" in error_msg:
        chatbot[-1] = (chatbot[-1][0], "[Local Message] System busy，Please try again in one minute。")
    else:
        from void_terminal.toolbox import regular_txt_to_markdown
        tb_str = '```\n' + trimmed_format_exc() + '```'
        chatbot[-1] = (chatbot[-1][0], f"[Local Message] Exception \n\n{tb_str} \n\n{regular_txt_to_markdown(chunk_decoded)}")
    return chatbot, history

def generate_payload(inputs, llm_kwargs, history, system_prompt, stream):
    """
    Integrate all information，Select LLM model，Generate http request，Prepare to send request
    """

    headers = {
        "Content-Type": "application/json",
    }

    conversation_cnt = len(history) // 2

    messages = [{"role": "system", "content": system_prompt}]
    if conversation_cnt:
        for index in range(0, 2*conversation_cnt, 2):
            what_i_have_asked = {}
            what_i_have_asked["role"] = "user"
            what_i_have_asked["content"] = history[index]
            what_gpt_answer = {}
            what_gpt_answer["role"] = "assistant"
            what_gpt_answer["content"] = history[index+1]
            if what_i_have_asked["content"] != "":
                if what_gpt_answer["content"] == "": continue
                if what_gpt_answer["content"] == timeout_bot_msg: continue
                messages.append(what_i_have_asked)
                messages.append(what_gpt_answer)
            else:
                messages[-1]['content'] = what_gpt_answer['content']

    what_i_ask_now = {}
    what_i_ask_now["role"] = "user"
    what_i_ask_now["content"] = inputs
    messages.append(what_i_ask_now)
    model = llm_kwargs['llm_model']
    if llm_kwargs['llm_model'].startswith('ollama-'):
        model = llm_kwargs['llm_model'][len('ollama-'):]
        model, _ = read_one_api_model_name(model)
    options = {"temperature": llm_kwargs['temperature']}
    payload = {
        "model": model,
        "messages": messages,
        "options": options,
    }
    try:
        print(f" {llm_kwargs['llm_model']} : {conversation_cnt} : {inputs[:100]} ..........")
    except:
        print('There may be garbled characters in the input。')
    return headers,payload
