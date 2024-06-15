# encoding: utf-8
# @Time   : 2023/12/21
# @Author : Spike
# @Descr   :
import json
import re
import os
import time
from void_terminal.request_llms.com_google import GoogleChatInit
from void_terminal.toolbox import ChatBotWithCookies
from void_terminal.toolbox import get_conf, update_ui, update_ui_lastest_msg, have_any_recent_upload_image_files, trimmed_format_exc, log_chat

proxies, TIMEOUT_SECONDS, MAX_RETRY = get_conf('proxies', 'TIMEOUT_SECONDS', 'MAX_RETRY')
timeout_bot_msg = '[Local Message] Request timeout. Network error. Please check proxy settings in config.py.' + \
                  'Network error，Check if the proxy server is available，And if the format of the proxy settings is correct，The format must be[Protocol]://[Address]:[Port]，All parts are necessary。'


def predict_no_ui_long_connection(inputs, llm_kwargs, history=[], sys_prompt="", observe_window=None,
                                  console_slience=False):
    # Check API_KEY
    if get_conf("GEMINI_API_KEY") == "":
        raise ValueError(f"Please Configure GEMINI_API_KEY。")

    genai = GoogleChatInit(llm_kwargs)
    watch_dog_patience = 5  # The patience of the watchdog, Set 5 seconds
    gpt_replying_buffer = ''
    stream_response = genai.generate_chat(inputs, llm_kwargs, history, sys_prompt)
    for response in stream_response:
        results = response.decode()
        match = re.search(r'"text":\s*"((?:[^"\\]|\\.)*)"', results, flags=re.DOTALL)
        error_match = re.search(r'\"message\":\s*\"(.*?)\"', results, flags=re.DOTALL)
        if match:
            try:
                paraphrase = json.loads('{"text": "%s"}' % match.group(1))
            except:
                raise ValueError(f"Error parsing GEMINI message。")
            buffer = paraphrase['text']
            gpt_replying_buffer += buffer
            if len(observe_window) >= 1:
                observe_window[0] = gpt_replying_buffer
            if len(observe_window) >= 2:
                if (time.time() - observe_window[1]) > watch_dog_patience: raise RuntimeError("Program terminated。")
        if error_match:
            raise RuntimeError(f'{gpt_replying_buffer} Dialogue Error')
    return gpt_replying_buffer


def predict(inputs:str, llm_kwargs:dict, plugin_kwargs:dict, chatbot:ChatBotWithCookies,
            history:list=[], system_prompt:str='', stream:bool=True, additional_fn:str=None):
    # Check API_KEY
    if get_conf("GEMINI_API_KEY") == "":
        yield from update_ui_lastest_msg(f"Please Configure GEMINI_API_KEY。", chatbot=chatbot, history=history, delay=0)
        return

    # Adapter polishing area
    if additional_fn is not None:
        from void_terminal.core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)

    if "vision" in llm_kwargs["llm_model"]:
        have_recent_file, image_paths = have_any_recent_upload_image_files(chatbot)
        if not have_recent_file:
            chatbot.append((inputs, "No recently uploaded image files detected，Please upload images in jpg format，In addition，Please note that the extension name needs to be lowercase"))
            yield from update_ui(chatbot=chatbot, history=history, msg="Waiting for image") # Refresh the page
            return
        def make_media_input(inputs, image_paths):
            for image_path in image_paths:
                inputs = inputs + f'<br/><br/><div align="center"><img src="file={os.path.abspath(image_path)}"></div>'
            return inputs
        if have_recent_file:
            inputs = make_media_input(inputs, image_paths)

    chatbot.append((inputs, ""))
    yield from update_ui(chatbot=chatbot, history=history)
    genai = GoogleChatInit(llm_kwargs)
    retry = 0
    while True:
        try:
            stream_response = genai.generate_chat(inputs, llm_kwargs, history, system_prompt)
            break
        except Exception as e:
            retry += 1
            chatbot[-1] = ((chatbot[-1][0], trimmed_format_exc()))
            yield from update_ui(chatbot=chatbot, history=history, msg="Request failed")  # Refresh the page
            return
    gpt_replying_buffer = ""
    gpt_security_policy = ""
    history.extend([inputs, ''])
    for response in stream_response:
        results = response.decode("utf-8")    # Fooled by this decoding。。
        gpt_security_policy += results
        match = re.search(r'"text":\s*"((?:[^"\\]|\\.)*)"', results, flags=re.DOTALL)
        error_match = re.search(r'\"message\":\s*\"(.*)\"', results, flags=re.DOTALL)
        if match:
            try:
                paraphrase = json.loads('{"text": "%s"}' % match.group(1))
            except:
                raise ValueError(f"Error parsing GEMINI message。")
            gpt_replying_buffer += paraphrase['text']    # Process using JSON parsing library
            chatbot[-1] = (inputs, gpt_replying_buffer)
            history[-1] = gpt_replying_buffer
            log_chat(llm_model=llm_kwargs["llm_model"], input_str=inputs, output_str=gpt_replying_buffer)
            yield from update_ui(chatbot=chatbot, history=history)
        if error_match:
            history = history[-2]  # Errors are not included in the conversation
            chatbot[-1] = (inputs, gpt_replying_buffer + f"Dialogue Error，Please check the message\n\n```\n{error_match.group(1)}\n```")
            yield from update_ui(chatbot=chatbot, history=history)
            raise RuntimeError('Dialogue Error')
    if not gpt_replying_buffer:
        history = history[-2]  # Errors are not included in the conversation
        chatbot[-1] = (inputs, gpt_replying_buffer + f"Triggered Google`s safe access policy，No answer\n\n```\n{gpt_security_policy}\n```")
        yield from update_ui(chatbot=chatbot, history=history)



if __name__ == '__main__':
    import sys
    llm_kwargs = {'llm_model': 'gemini-pro'}
    result = predict('Write long a story about a magic backpack.', llm_kwargs, llm_kwargs, [])
    for i in result:
        print(i)
