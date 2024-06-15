# In this source code, ⭐ = Key step
"""
Test：
    - show me the solution of $x^2=cos(x)$, solve this problem with figure, and plot and save image to t.jpg

"""


from void_terminal.toolbox import CatchException, update_ui, gen_time_str, trimmed_format_exc, ProxyNetworkActivate
from void_terminal.toolbox import get_conf, select_api_key, update_ui_lastest_msg, Singleton
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive, get_plugin_arg
from void_terminal.crazy_functions.crazy_utils import input_clipping, try_install_deps
from void_terminal.crazy_functions.agent_fns.persistent import GradioMultiuserManagerForPersistentClasses
from void_terminal.crazy_functions.agent_fns.auto_agent import AutoGenMath
import time

def remove_model_prefix(llm):
    if llm.startswith('api2d-'): llm = llm.replace('api2d-', '')
    if llm.startswith('azure-'): llm = llm.replace('azure-', '')
    return llm


@CatchException
def MultiAgentTerminal(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    """
    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters，Such as temperature and top_p，Generally pass it on as is
    plugin_kwargs   Plugin model parameters
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    user_request    Current user`s request information（IP addresses, etc.）
    """
    # Check if the current model meets the requirements
    supported_llms = [
        "gpt-3.5-turbo-16k",
        'gpt-3.5-turbo-1106',
        "gpt-4",
        "gpt-4-32k",
        'gpt-4-1106-preview',
        "azure-gpt-3.5-turbo-16k",
        "azure-gpt-3.5-16k",
        "azure-gpt-4",
        "azure-gpt-4-32k",
    ]
    from void_terminal.request_llms.bridge_all import model_info
    if model_info[llm_kwargs['llm_model']]["max_token"] < 8000: # A model with at least 8k context
        chatbot.append([f"Process task: {txt}", f"The current plugin only supports{str(supported_llms)}, Current model{llm_kwargs['llm_model']}The maximum context length is too short, Cannot support AutoGen operation。"])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return
    if model_info[llm_kwargs['llm_model']]["endpoint"] is not None: # If it is not a local model，Loading API_KEY
        llm_kwargs['api_key'] = select_api_key(llm_kwargs['api_key'], llm_kwargs['llm_model'])

    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
    try:
        import autogen
        if get_conf("AUTOGEN_USE_DOCKER"):
            import docker
    except:
        chatbot.append([ f"Process task: {txt}",
            f"Failed to import software dependencies。Using this module requires additional dependencies，Installation method```pip install --upgrade pyautogen docker```。"])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
    try:
        import autogen
        import glob, os, time, subprocess
        if get_conf("AUTOGEN_USE_DOCKER"):
            subprocess.Popen(["docker", "--version"])
    except:
        chatbot.append([f"Process task: {txt}", f"Missing docker runtime environment!"])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Unlock plugin
    chatbot.get_cookies()['lock_plugin'] = None
    persistent_class_multi_user_manager = GradioMultiuserManagerForPersistentClasses()
    user_uuid = chatbot.get_cookies().get('uuid')
    persistent_key = f"{user_uuid}->MultiAgentTerminal"
    if persistent_class_multi_user_manager.already_alive(persistent_key):
        # When there is already a running MultiAgentTerminal，Pass user input directly to it，Instead of starting a new MultiAgentTerminal again
        print('[debug] feed new user input')
        executor = persistent_class_multi_user_manager.get(persistent_key)
        exit_reason = yield from executor.main_process_ui_control(txt, create_or_resume="resume")
    else:
        # Run MultiAgentTerminal (For the first time)
        print('[debug] create new executor instance')
        history = []
        chatbot.append(["Starting: MultiAgentTerminal", "Dynamic generation of plugins, Execution starts, Author Microsoft & Binary-Husky."])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        executor = AutoGenMath(llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request)
        persistent_class_multi_user_manager.set(persistent_key, executor)
        exit_reason = yield from executor.main_process_ui_control(txt, create_or_resume="create")

    if exit_reason == "wait_feedback":
        # When the user clicks the `Wait for Feedback` button，Store the executor in the cookie，Waiting for the user to call again
        executor.chatbot.get_cookies()['lock_plugin'] = 'crazy_functions.MultiAgent->MultiAgentTerminal'
    else:
        executor.chatbot.get_cookies()['lock_plugin'] = None
    yield from update_ui(chatbot=executor.chatbot, history=executor.history) # Update status
