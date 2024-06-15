import time
import os
from void_terminal.toolbox import update_ui, get_conf, update_ui_lastest_msg
from void_terminal.toolbox import check_packages, report_exception

model_name = 'Qwen'

def predict_no_ui_long_connection(inputs:str, llm_kwargs:dict, history:list=[], sys_prompt:str="",
                                  observe_window:list=[], console_slience:bool=False):
    """
        ⭐Multi-threaded method
        For function details, please see request_llms/bridge_all.py
    """
    watch_dog_patience = 5
    response = ""

    from void_terminal.request_llms.com_qwenapi import QwenRequestInstance
    sri = QwenRequestInstance()
    for response in sri.generate(inputs, llm_kwargs, history, sys_prompt):
        if len(observe_window) >= 1:
            observe_window[0] = response
        if len(observe_window) >= 2:
            if (time.time()-observe_window[1]) > watch_dog_patience: raise RuntimeError("Program terminated。")
    return response

def predict(inputs, llm_kwargs, plugin_kwargs, chatbot, history=[], system_prompt='', stream = True, additional_fn=None):
    """
        ⭐Single-threaded method
        For function details, please see request_llms/bridge_all.py
    """
    chatbot.append((inputs, ""))
    yield from update_ui(chatbot=chatbot, history=history)

    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
    try:
        check_packages(["dashscope"])
    except:
        yield from update_ui_lastest_msg(f"Failed to import software dependencies。TranslatedText，Installation method```pip install --upgrade dashscope```。",
                                         chatbot=chatbot, history=history, delay=0)
        return

    # Check DASHSCOPE_API_KEY
    if get_conf("DASHSCOPE_API_KEY") == "":
        yield from update_ui_lastest_msg(f"Please Configure DASHSCOPE_API_KEY。",
                                         chatbot=chatbot, history=history, delay=0)
        return

    if additional_fn is not None:
        from void_terminal.core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)
        chatbot[-1] = (inputs, "")
        yield from update_ui(chatbot=chatbot, history=history)

    # Start receiving replies
    from void_terminal.request_llms.com_qwenapi import QwenRequestInstance
    sri = QwenRequestInstance()
    response = f"[Local Message] Waiting{model_name}Responding ..."
    for response in sri.generate(inputs, llm_kwargs, history, system_prompt):
        chatbot[-1] = (inputs, response)
        yield from update_ui(chatbot=chatbot, history=history)

    # Summary output
    if response == f"[Local Message] Waiting{model_name}Responding ...":
        response = f"[Local Message] {model_name}Response exception ..."
    history.extend([inputs, response])
    yield from update_ui(chatbot=chatbot, history=history)