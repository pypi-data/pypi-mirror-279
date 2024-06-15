# encoding: utf-8
# @Time   : 2023/4/19
# @Author : Spike
# @Descr   :
from void_terminal.toolbox import update_ui, get_conf, get_user
from void_terminal.toolbox import CatchException
from void_terminal.toolbox import default_user_name
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
import shutil
import os


@CatchException
def 猜你想Ask(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    if txt:
        show_say = txt
        prompt = txt+'\nAfter answering the question，List three more questions that the user might ask。'
    else:
        prompt = history[-1]+"\nAnalyze the above answer，List three more questions that the user might ask。"
        show_say = 'Analyze the above answer，List three more questions that the user might ask。'
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=prompt,
        inputs_show_user=show_say,
        llm_kwargs=llm_kwargs,
        chatbot=chatbot,
        history=history,
        sys_prompt=system_prompt
    )
    chatbot[-1] = (show_say, gpt_say)
    history.extend([show_say, gpt_say])
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page


@CatchException
def ClearCache(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    chatbot.append(['Clear local cache data', 'Executing. Deleting data'])
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page

    def _get_log_folder(user=default_user_name):
        PATH_LOGGING = get_conf('PATH_LOGGING')
        _dir = os.path.join(PATH_LOGGING, user)
        if not os.path.exists(_dir): os.makedirs(_dir)
        return _dir

    def _get_upload_folder(user=default_user_name):
        PATH_PRIVATE_UPLOAD = get_conf('PATH_PRIVATE_UPLOAD')
        _dir = os.path.join(PATH_PRIVATE_UPLOAD, user)
        return _dir

    shutil.rmtree(_get_log_folder(get_user(chatbot)), ignore_errors=True)
    shutil.rmtree(_get_upload_folder(get_user(chatbot)), ignore_errors=True)

    chatbot.append(['Clear local cache data', 'Execution completed'])
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page