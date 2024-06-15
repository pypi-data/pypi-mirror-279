import time
import os
from void_terminal.toolbox import update_ui, get_conf, update_ui_lastest_msg, log_chat
from void_terminal.toolbox import check_packages, report_exception, have_any_recent_upload_image_files
from void_terminal.toolbox import ChatBotWithCookies

model_name = 'Zhipu AI large model'
zhipuai_default_model = 'glm-4'

def validate_key():
    ZHIPUAI_API_KEY = get_conf("ZHIPUAI_API_KEY")
    if ZHIPUAI_API_KEY == '': return False
    return True

def make_media_input(inputs, image_paths):
    for image_path in image_paths:
        inputs = inputs + f'<br/><br/><div align="center"><img src="file={os.path.abspath(image_path)}"></div>'
    return inputs

def predict_no_ui_long_connection(inputs:str, llm_kwargs:dict, history:list=[], sys_prompt:str="",
                                  observe_window:list=[], console_slience:bool=False):
    """
        ⭐Multi-threaded method
        For function details, please see request_llms/bridge_all.py
    """
    watch_dog_patience = 5
    response = ""

    if llm_kwargs["llm_model"] == "zhipuai":
        llm_kwargs["llm_model"] = zhipuai_default_model

    if validate_key() is False:
        raise RuntimeError('Please configure ZHIPUAI_API_KEY')

    # Start receiving replies
    from void_terminal.request_llms.com_zhipuglm import ZhipuChatInit
    zhipu_bro_init = ZhipuChatInit()
    for chunk, response in zhipu_bro_init.generate_chat(inputs, llm_kwargs, history, sys_prompt):
        if len(observe_window) >= 1:
            observe_window[0] = response
        if len(observe_window) >= 2:
            if (time.time() - observe_window[1]) > watch_dog_patience:
                raise RuntimeError("Program terminated。")
    return response


def predict(inputs:str, llm_kwargs:dict, plugin_kwargs:dict, chatbot:ChatBotWithCookies,
            history:list=[], system_prompt:str='', stream:bool=True, additional_fn:str=None):
    """
        ⭐Single-threaded method
        For function details, please see request_llms/bridge_all.py
    """
    chatbot.append([inputs, ""])
    yield from update_ui(chatbot=chatbot, history=history)

    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
    try:
        check_packages(["zhipuai"])
    except:
        yield from update_ui_lastest_msg(f"Failed to import software dependencies。TranslatedText，Installation method```pip install --upgrade zhipuai```。",
            chatbot=chatbot, history=history, delay=0)
        return

    if validate_key() is False:
        yield from update_ui_lastest_msg(lastmsg="[Local Message] Please configure ZHIPUAI_API_KEY", chatbot=chatbot, history=history, delay=0)
        return

    if additional_fn is not None:
        from void_terminal.core_functional import handle_core_functionality
        inputs, history = handle_core_functionality(additional_fn, inputs, history, chatbot)
        chatbot[-1] = [inputs, ""]
        yield from update_ui(chatbot=chatbot, history=history)

    if llm_kwargs["llm_model"] == "zhipuai":
        llm_kwargs["llm_model"] = zhipuai_default_model

    if llm_kwargs["llm_model"] in ["glm-4v"]:
        if (len(inputs) + sum(len(temp) for temp in history) + 1047) > 2000:
            chatbot.append((inputs, "The context length exceeds the upper limit of 2000 tokens for glm-4v，Note that the image takes up about 1,47 tokens"))
            yield from update_ui(chatbot=chatbot, history=history)
            return
        have_recent_file, image_paths = have_any_recent_upload_image_files(chatbot)
        if not have_recent_file:
            chatbot.append((inputs, "No recently uploaded image files detected，Please upload images in jpg format，In addition，Please note that the extension name needs to be lowercase"))
            yield from update_ui(chatbot=chatbot, history=history, msg="Waiting for image") # Refresh the page
            return
        if have_recent_file:
            inputs = make_media_input(inputs, image_paths)
            chatbot[-1] = [inputs, ""]
            yield from update_ui(chatbot=chatbot, history=history)


    # Start receiving replies
    from void_terminal.request_llms.com_zhipuglm import ZhipuChatInit
    zhipu_bro_init = ZhipuChatInit()
    for chunk, response in zhipu_bro_init.generate_chat(inputs, llm_kwargs, history, system_prompt):
        chatbot[-1] = [inputs, response]
        yield from update_ui(chatbot=chatbot, history=history)
    history.extend([inputs, response])
    log_chat(llm_model=llm_kwargs["llm_model"], input_str=inputs, output_str=response)
    yield from update_ui(chatbot=chatbot, history=history)