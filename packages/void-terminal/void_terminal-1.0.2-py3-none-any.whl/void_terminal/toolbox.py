import importlib
import time
import inspect
import re
import os
import base64
import fake_gradio as gradio
import shutil
import glob
import logging
import uuid
from functools import wraps
from void_terminal.shared_utils.config_loader import get_conf
from void_terminal.shared_utils.config_loader import set_conf
from void_terminal.shared_utils.config_loader import set_multi_conf
from void_terminal.shared_utils.config_loader import read_single_conf_with_lru_cache
from void_terminal.shared_utils.advanced_markdown_format import format_io
from void_terminal.shared_utils.advanced_markdown_format import markdown_convertion
from void_terminal.shared_utils.key_pattern_manager import select_api_key
from void_terminal.shared_utils.key_pattern_manager import is_any_api_key
from void_terminal.shared_utils.key_pattern_manager import what_keys
from void_terminal.shared_utils.connect_void_terminal import get_chat_handle
from void_terminal.shared_utils.connect_void_terminal import get_plugin_handle
from void_terminal.shared_utils.connect_void_terminal import get_plugin_default_kwargs
from void_terminal.shared_utils.connect_void_terminal import get_chat_default_kwargs
from void_terminal.shared_utils.text_mask import apply_gpt_academic_string_mask
from void_terminal.shared_utils.text_mask import build_gpt_academic_masked_string
from void_terminal.shared_utils.text_mask import apply_gpt_academic_string_mask_langbased
from void_terminal.shared_utils.text_mask import build_gpt_academic_masked_string_langbased
from void_terminal.shared_utils.map_names import map_friendly_names_to_model
from void_terminal.shared_utils.map_names import map_model_to_friendly_names
from void_terminal.shared_utils.map_names import read_one_api_model_name
from void_terminal.shared_utils.handle_upload import html_local_file
from void_terminal.shared_utils.handle_upload import html_local_img
from void_terminal.shared_utils.handle_upload import file_manifest_filter_type
from void_terminal.shared_utils.handle_upload import extract_archive
from typing import List
pj = os.path.join
default_user_name = "default_user"

"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
First part
Function plugin input and output docking area
    - ChatBotWithCookies:   Chatbot class with cookies，Laying the foundation for implementing more powerful functions
    - ArgsGeneralWrapper:   Decorator function，Used to restructure input parameters，Change the order and structure of input parameters
    - update_ui:            Refresh the interface using yield from update_ui(chatbot, history)
    - CatchException:       Display all questions from the plugin on the interface
    - HotReload:            Implement hot update of the plugin
    - trimmed_format_exc:   Print traceback，Hide absolute address for security reasons
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


class ChatBotWithCookies(list):
    def __init__(self, cookie):
        """
        cookies = {
            'top_p': top_p,
            'temperature': temperature,
            'lock_plugin': bool,
            "files_to_promote": ["file1", "file2"],
            "most_recent_uploaded": {
                "path": "uploaded_path",
                "time": time.time(),
                "time_str": "timestr",
            }
        }
        """
        self._cookies = cookie

    def write_list(self, list):
        for t in list:
            self.append(t)

    def get_list(self):
        return [t for t in self]

    def get_cookies(self):
        return self._cookies

    def get_user(self):
        return self._cookies.get("user_name", default_user_name)

def ArgsGeneralWrapper(f):
    """
    Decorator function ArgsGeneralWrapper，Used to restructure input parameters，Change the order and structure of input parameters。
    This decorator is the entry point for most function calls。
    Function Diagram：https://mermaid.live/edit#pako:eNqNVFtPGkEY_StkntoEDQtLoTw0sWqapjQxVWPabmOm7AiEZZcsQ9QiiW012qixqdeqqIn10geBh6ZR8PJnmAWe-hc6l3VhrWnLEzNzzvnO953ZyYOYoSIQAWOaMR5LQBN7hvoU3UN_g5iu7imAXEyT4wUF3Pd0dT3y9KGYYUJsmK8V0GPGs0-QjkyojZgwk0Fm82C2dVghX08U8EaoOHjOfoEMU0XmADRhOksVWnNLjdpM82qFzB6S5Q_WWsUhuqCc3JtAsVR_OoMnhyZwXgHWwbS1d4gnsLVZJp-P6mfVxveqAgqC70Jz_pQCOGDKM5xFdNNPDdilF6uSU_hOYqu4a3MHYDZLDzq5fodrC3PWcEaFGPUaRiqJWK_W9g9rvRITa4dhy_0nw67SiePMp3oSR6PPn41DGgllkvkizYwsrmtaejTFd8V4yekGmT1zqrt4XGlAy8WTuiPULF01LksZvukSajfQQRAxmYi5S0D81sDcyzapVdn6sYFHkjhhGyel3frVQnvsnbR23lEjlhIlaOJiFPWzU5G4tfNJo8ejwp47-TbvJkKKZvmxA6SKo16oaazJysfG6klr9T0pbTW2ZqzlL_XaT8fYbQLXe4mSmvoCZXMaa7FePW6s7jVqK9bujvse3WFjY5_Z4KfsA4oiPY4T7Drvn1tLJTbG1to1qR79ulgk89-oJbvZzbIwJty6u20LOReWa9BvwserUd9s9MIKc3x5TUWEoAhUyJK5y85w_yG-dFu_R9waoU7K581y8W_qLle35-rG9Nxcrz8QHRsc0K-r9NViYRT36KsFvCCNzDRMqvSVyzOKAnACpZECIvSvCs2UAhS9QHEwh43BST0GItjMIS_I8e-sLwnj9A262cxA_ZVh0OUY1LJiDSJ5MAEiUijYLUtBORR6KElyQPaCSRDpksNSd8AfluSgHPaFC17wjrOlbgbzyyFf4IFPDvoD_sJvnkdK-g
    """
    def decorated(request: gradio.Request, cookies:dict, max_length:int, llm_model:str,
                  txt:str, txt2:str, top_p:float, temperature:float, chatbot:list,
                  history:list, system_prompt:str, plugin_advanced_arg:dict, *args):
        txt_passon = txt
        if txt == "" and txt2 != "": txt_passon = txt2
        # Introduce a chatbot with cookies
        if request.username is not None:
            user_name = request.username
        else:
            user_name = default_user_name
        cookies.update({
            'top_p': top_p,
            'api_key': cookies['api_key'],
            'llm_model': llm_model,
            'temperature': temperature,
            'user_name': user_name,
        })
        llm_kwargs = {
            'api_key': cookies['api_key'],
            'llm_model': llm_model,
            'top_p': top_p,
            'max_length': max_length,
            'temperature': temperature,
            'client_ip': request.client.host,
            'most_recent_uploaded': cookies.get('most_recent_uploaded')
        }
        if isinstance(plugin_advanced_arg, str):
            plugin_kwargs = {"advanced_arg": plugin_advanced_arg}
        else:
            plugin_kwargs = plugin_advanced_arg
        chatbot_with_cookie = ChatBotWithCookies(cookies)
        chatbot_with_cookie.write_list(chatbot)

        if cookies.get('lock_plugin', None) is None:
            # Normal state
            if len(args) == 0:  # Plugin channel
                yield from f(txt_passon, llm_kwargs, plugin_kwargs, chatbot_with_cookie, history, system_prompt, request)
            else:               # Conversation channel，Or the basic function channel
                yield from f(txt_passon, llm_kwargs, plugin_kwargs, chatbot_with_cookie, history, system_prompt, *args)
        else:
            # Handle the locked state of special plugins in a few cases
            module, fn_name = cookies['lock_plugin'].split('->')
            f_hot_reload = getattr(importlib.import_module(module, fn_name), fn_name)
            yield from f_hot_reload(txt_passon, llm_kwargs, plugin_kwargs, chatbot_with_cookie, history, system_prompt, request)
            # Check if the user entered through the dialogue channel by mistake，If it is，Then remind
            final_cookies = chatbot_with_cookie.get_cookies()
            # len(args) != 0 represents the `Submit` key dialogue channel，Or the basic function channel
            if len(args) != 0 and 'files_to_promote' in final_cookies and len(final_cookies['files_to_promote']) > 0:
                chatbot_with_cookie.append(
                    ["Detected **stuck cache document**，Please handle it in time。", "Please click `**Save Current Dialogue**` in time to obtain all cached documents。"])
                yield from update_ui(chatbot_with_cookie, final_cookies['history'], msg="Detected cached documents being left behind")

    return decorated


def update_ui(chatbot:ChatBotWithCookies, history, msg="Normal", **kwargs):  # Refresh the page
    """
    Refresh the user interface
    """
    assert isinstance(
        chatbot, ChatBotWithCookies
    ), "Do not discard it when passing the chatbot。If necessary, It can be cleared with clear if necessary, Then reassign with for+append loop。"
    cookies = chatbot.get_cookies()
    # Backup a copy of History as a record
    cookies.update({"history": history})
    # Solve the interface display problem when the plugin is locked
    if cookies.get("lock_plugin", None):
        label = (
            cookies.get("llm_model", "")
            + " | "
            + "Locking plugin"
            + cookies.get("lock_plugin", None)
        )
        chatbot_gr = gradio.update(value=chatbot, label=label)
        if cookies.get("label", "") != label:
            cookies["label"] = label  # Remember the current label.
    elif cookies.get("label", None):
        chatbot_gr = gradio.update(value=chatbot, label=cookies.get("llm_model", ""))
        cookies["label"] = None  # Clear label
    else:
        chatbot_gr = chatbot

    yield cookies, chatbot_gr, history, msg


def update_ui_lastest_msg(lastmsg:str, chatbot:ChatBotWithCookies, history:list, delay=1):  # Refresh the page
    """
    Refresh the user interface
    """
    if len(chatbot) == 0:
        chatbot.append(["update_ui_last_msg", lastmsg])
    chatbot[-1] = list(chatbot[-1])
    chatbot[-1][-1] = lastmsg
    yield from update_ui(chatbot=chatbot, history=history)
    time.sleep(delay)


def trimmed_format_exc():
    import os, traceback

    str = traceback.format_exc()
    current_path = os.getcwd()
    replace_path = "."
    return str.replace(current_path, replace_path)

def trimmed_format_exc_markdown():
    return '\n\n```\n' + trimmed_format_exc() + '```'

def CatchException(f):
    """
    Decorator function，Capture exceptions in function f and encapsulate them into a generator to return，And display it in the chat。
    """

    @wraps(f)
    def decorated(main_input:str, llm_kwargs:dict, plugin_kwargs:dict,
                  chatbot_with_cookie:ChatBotWithCookies, history:list, *args, **kwargs):
        try:
            yield from f(main_input, llm_kwargs, plugin_kwargs, chatbot_with_cookie, history, *args, **kwargs)
        except Exception as e:
            from void_terminal.toolbox import get_conf
            tb_str = '```\n' + trimmed_format_exc() + '```'
            if len(chatbot_with_cookie) == 0:
                chatbot_with_cookie.clear()
                chatbot_with_cookie.append(["Plugin scheduling exception", "Exception reason"])
            chatbot_with_cookie[-1] = (chatbot_with_cookie[-1][0], f"[Local Message] Plugin call error: \n\n{tb_str} \n")
            yield from update_ui(chatbot=chatbot_with_cookie, history=history, msg=f'Exception {e}')  # Refresh the page

    return decorated


def HotReload(f):
    """
    Decorator function of HotReload，Used to implement hot updates of Python function plugins。
    Function hot update refers to updating function code in real-time without stopping program execution，Update function code，To achieve real-time update function。
    Inside the decorator，Use wraps(f)Preserve the metadata of the function，and define an inner function named decorated。
    The inner function reloads and retrieves the function module by using the reload function of the importlib module and the getmodule function of the inspect module，
    Then it retrieves the function name using the getattr function，and reloads the function in the new module。
    Finally，it returns the reloaded function using the yield from statement，and executes it on the decorated function。
    Ultimately，the decorator function returns the inner function。which can update the original definition of the function to the latest version，and execute the new version of the function。
    """
    if get_conf("PLUGIN_HOT_RELOAD"):

        @wraps(f)
        def decorated(*args, **kwargs):
            fn_name = f.__name__
            f_hot_reload = getattr(importlib.reload(inspect.getmodule(f)), fn_name)
            yield from f_hot_reload(*args, **kwargs)

        return decorated
    else:
        return f


"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
Second part
Other utilities:
    - write_history_to_file:    Write the results to a markdown file
    - regular_txt_to_markdown:  Convert plain text to Markdown formatted text。
    - report_exception:         Add simple unexpected error messages to the chatbot
    - text_divide_paragraph:    Split the text into paragraphs according to the paragraph separator，Generate HTML code with paragraph tags。
    - markdown_convertion:      Combine in various ways，Convert markdown to nice-looking HTML
    - format_io:                Take over the default markdown handling of gradio
    - on_file_uploaded:         Handle file uploads（Automatically decompress）
    - on_report_generated:      Automatically project the generated report to the file upload area
    - clip_history:             Automatically truncate when the historical context is too long，Automatic truncation
    - get_conf:                 Get settings
    - select_api_key:           According to the current model category，Extract available API keys
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


def get_reduce_token_percent(text:str):
    """
    * This function will be deprecated in the future
    """
    try:
        # text = "maximum context length is 4097 tokens. However, your messages resulted in 4870 tokens"
        pattern = r"(\d+)\s+tokens\b"
        match = re.findall(pattern, text)
        EXCEED_ALLO = 500  # Leave a little room，Otherwise, there will be problems with insufficient space when replying
        max_limit = float(match[0]) - EXCEED_ALLO
        current_tokens = float(match[1])
        ratio = max_limit / current_tokens
        assert ratio > 0 and ratio < 1
        return ratio, str(int(current_tokens - max_limit))
    except:
        return 0.5, "Unknown"


def write_history_to_file(
    history:list, file_basename:str=None, file_fullname:str=None, auto_caption:bool=True
):
    """
    Write the conversation record history to a file in Markdown format。If no file name is specified，Generate a file name using the current time。
    """
    import os
    import time

    if file_fullname is None:
        if file_basename is not None:
            file_fullname = pj(get_log_folder(), file_basename)
        else:
            file_fullname = pj(get_log_folder(), f"GPT-Academic-{gen_time_str()}.md")
    os.makedirs(os.path.dirname(file_fullname), exist_ok=True)
    with open(file_fullname, "w", encoding="utf8") as f:
        f.write("# GPT-Academic Report\n")
        for i, content in enumerate(history):
            try:
                if type(content) != str:
                    content = str(content)
            except:
                continue
            if i % 2 == 0 and auto_caption:
                f.write("## ")
            try:
                f.write(content)
            except:
                # remove everything that cannot be handled by utf8
                f.write(content.encode("utf-8", "ignore").decode())
            f.write("\n\n")
    res = os.path.abspath(file_fullname)
    return res


def regular_txt_to_markdown(text:str):
    """
    Convert plain text to Markdown formatted text。
    """
    text = text.replace("\n", "\n\n")
    text = text.replace("\n\n\n", "\n\n")
    text = text.replace("\n\n\n", "\n\n")
    return text


def report_exception(chatbot:ChatBotWithCookies, history:list, a:str, b:str):
    """
    Add error information to the chatbot
    """
    chatbot.append((a, b))
    history.extend([a, b])


def find_free_port()->int:
    """
    Return an available unused port in the current system。
    """
    import socket
    from contextlib import closing

    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def find_recent_files(directory:str)->List[str]:
    """
    Find files that is created with in one minutes under a directory with python, write a function
    """
    import os
    import time

    current_time = time.time()
    one_minute_ago = current_time - 60
    recent_files = []
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    for filename in os.listdir(directory):
        file_path = pj(directory, filename)
        if file_path.endswith(".log"):
            continue
        created_time = os.path.getmtime(file_path)
        if created_time >= one_minute_ago:
            if os.path.isdir(file_path):
                continue
            recent_files.append(file_path)

    return recent_files


def file_already_in_downloadzone(file:str, user_path:str):
    try:
        parent_path = os.path.abspath(user_path)
        child_path = os.path.abspath(file)
        if os.path.samefile(os.path.commonpath([parent_path, child_path]), parent_path):
            return True
        else:
            return False
    except:
        return False


def promote_file_to_downloadzone(file:str, rename_file:str=None, chatbot:ChatBotWithCookies=None):
    # Make a copy of the file in the download area
    import shutil

    if chatbot is not None:
        user_name = get_user(chatbot)
    else:
        user_name = default_user_name
    if not os.path.exists(file):
        raise FileNotFoundError(f"File{file}Does not exist")
    user_path = get_log_folder(user_name, plugin_name=None)
    if file_already_in_downloadzone(file, user_path):
        new_path = file
    else:
        user_path = get_log_folder(user_name, plugin_name="downloadzone")
        if rename_file is None:
            rename_file = f"{gen_time_str()}-{os.path.basename(file)}"
        new_path = pj(user_path, rename_file)
        # If it already exists，Delete first
        if os.path.exists(new_path) and not os.path.samefile(new_path, file):
            os.remove(new_path)
        # Copy the file over
        if not os.path.exists(new_path):
            shutil.copyfile(file, new_path)
    # Add files to chatbot cookie
    if chatbot is not None:
        if "files_to_promote" in chatbot._cookies:
            current = chatbot._cookies["files_to_promote"]
        else:
            current = []
        if new_path not in current:  # Avoid adding the same file multiple times
            chatbot._cookies.update({"files_to_promote": [new_path] + current})
    return new_path


def disable_auto_promotion(chatbot:ChatBotWithCookies):
    chatbot._cookies.update({"files_to_promote": []})
    return


def del_outdated_uploads(outdate_time_seconds:float, target_path_base:str=None):
    if target_path_base is None:
        user_upload_dir = get_conf("PATH_PRIVATE_UPLOAD")
    else:
        user_upload_dir = target_path_base
    current_time = time.time()
    one_hour_ago = current_time - outdate_time_seconds
    # Get a list of all subdirectories in the user_upload_dir folder
    # Remove subdirectories that are older than one hour
    for subdirectory in glob.glob(f"{user_upload_dir}/*"):
        subdirectory_time = os.path.getmtime(subdirectory)
        if subdirectory_time < one_hour_ago:
            try:
                shutil.rmtree(subdirectory)
            except:
                pass
    return



def to_markdown_tabs(head: list, tabs: list, alignment=":---:", column=False, omit_path=None):
    """
    Args:
        head: Table header：[]
        tabs: Table value：[[TranslatedText], [Column 2], [TranslatedText], [TranslatedText]]
        alignment: :--- Left alignment， :---: Center alignment， ---: Right alignment
        column: True to keep data in columns, False to keep data in rows (default).
    Returns:
        A string representation of the markdown table.
    """
    if column:
        transposed_tabs = list(map(list, zip(*tabs)))
    else:
        transposed_tabs = tabs
    # Find the maximum length among the columns
    max_len = max(len(column) for column in transposed_tabs)

    tab_format = "| %s "
    tabs_list = "".join([tab_format % i for i in head]) + "|\n"
    tabs_list += "".join([tab_format % alignment for i in head]) + "|\n"

    for i in range(max_len):
        row_data = [tab[i] if i < len(tab) else "" for tab in transposed_tabs]
        row_data = file_manifest_filter_type(row_data, filter_=None)
        # for dat in row_data:
        #     if (omit_path is not None) and os.path.exists(dat):
        #         dat = os.path.relpath(dat, omit_path)
        tabs_list += "".join([tab_format % i for i in row_data]) + "|\n"

    return tabs_list


def on_file_uploaded(
    request: gradio.Request, files:List[str], chatbot:ChatBotWithCookies,
    txt:str, txt2:str, checkboxes:List[str], cookies:dict
):
    """
    Callback function when a file is uploaded
    """
    if len(files) == 0:
        return chatbot, txt

    # Create a working directory
    user_name = default_user_name if not request.username else request.username
    time_tag = gen_time_str()
    target_path_base = get_upload_folder(user_name, tag=time_tag)
    os.makedirs(target_path_base, exist_ok=True)

    # Remove outdated old files to save space & protect privacy
    outdate_time_seconds = 3600  # One hour
    del_outdated_uploads(outdate_time_seconds, get_upload_folder(user_name))

    # Move each file to the target path
    upload_msg = ""
    for file in files:
        file_origin_name = os.path.basename(file.orig_name)
        this_file_path = pj(target_path_base, file_origin_name)
        shutil.move(file.name, this_file_path)
        upload_msg += extract_archive(
            file_path=this_file_path, dest_dir=this_file_path + ".extract"
        )

    # Organize file collection and output message
    files = glob.glob(f"{target_path_base}/**/*", recursive=True)
    moved_files = [fp for fp in files]
    max_file_to_show = 10
    if len(moved_files) > max_file_to_show:
        moved_files = moved_files[:max_file_to_show//2] + [f'... ( Omit{len(moved_files) - max_file_to_show}Display of a file ) ...'] + \
                      moved_files[-max_file_to_show//2:]
    moved_files_str = to_markdown_tabs(head=["File"], tabs=[moved_files], omit_path=target_path_base)
    chatbot.append(
        [
            "I uploaded a file，Please check",
            f"[Local Message] Received the following files （Upload to path：{target_path_base}）: " +
            f"\n\n{moved_files_str}" +
            f"\n\nThe call path parameter has been automatically corrected to: \n\n{txt}" +
            f"\n\nNow when you click on any function plugin，The above files will be used as input parameters" +
            upload_msg,
        ]
    )

    txt, txt2 = target_path_base, ""
    if "Floating input area" in checkboxes:
        txt, txt2 = txt2, txt

    # Record recent files
    cookies.update(
        {
            "most_recent_uploaded": {
                "path": target_path_base,
                "time": time.time(),
                "time_str": time_tag,
            }
        }
    )
    return chatbot, txt, txt2, cookies


def generate_file_link(report_files:List[str]):
    file_links = ""
    for f in report_files:
        file_links += (
            f'<br/><a href="file={os.path.abspath(f)}" target="_blank">{f}</a>'
        )
    return file_links




def on_report_generated(cookies:dict, files:List[str], chatbot:ChatBotWithCookies):
    if "files_to_promote" in cookies:
        report_files = cookies["files_to_promote"]
        cookies.pop("files_to_promote")
    else:
        report_files = []
    if len(report_files) == 0:
        return cookies, None, chatbot
    file_links = ""
    for f in report_files:
        file_links += (
            f'<br/><a href="file={os.path.abspath(f)}" target="_blank">{f}</a>'
        )
    chatbot.append(["Report how to obtain remotely？", f"The report has been added to the right `File Download Area`（It may be in a collapsed state），Please check。{file_links}"])
    return cookies, report_files, chatbot


def load_chat_cookies():
    API_KEY, LLM_MODEL, AZURE_API_KEY = get_conf(
        "API_KEY", "LLM_MODEL", "AZURE_API_KEY"
    )
    AZURE_CFG_ARRAY, NUM_CUSTOM_BASIC_BTN = get_conf(
        "AZURE_CFG_ARRAY", "NUM_CUSTOM_BASIC_BTN"
    )

    # deal with azure openai key
    if is_any_api_key(AZURE_API_KEY):
        if is_any_api_key(API_KEY):
            API_KEY = API_KEY + "," + AZURE_API_KEY
        else:
            API_KEY = AZURE_API_KEY
    if len(AZURE_CFG_ARRAY) > 0:
        for azure_model_name, azure_cfg_dict in AZURE_CFG_ARRAY.items():
            if not azure_model_name.startswith("azure"):
                raise ValueError("The models configured in AZURE_CFG_ARRAY must start with `azure`")
            AZURE_API_KEY_ = azure_cfg_dict["AZURE_API_KEY"]
            if is_any_api_key(AZURE_API_KEY_):
                if is_any_api_key(API_KEY):
                    API_KEY = API_KEY + "," + AZURE_API_KEY_
                else:
                    API_KEY = AZURE_API_KEY_

    customize_fn_overwrite_ = {}
    for k in range(NUM_CUSTOM_BASIC_BTN):
        customize_fn_overwrite_.update(
            {
                "Custom button"
                + str(k + 1): {
                    "Title": r"",
                    "Prefix": r"Please define the prefix of the prompt word in the custom menu.",
                    "Suffix": r"Please define the suffix of the prompt word in the custom menu",
                }
            }
        )
    return {
        "api_key": API_KEY,
        "llm_model": LLM_MODEL,
        "customize_fn_overwrite": customize_fn_overwrite_,
    }


def clear_line_break(txt):
    txt = txt.replace("\n", " ")
    txt = txt.replace("  ", " ")
    txt = txt.replace("  ", " ")
    return txt


class DummyWith:
    """
    This code defines an empty context manager named DummyWith，
    Its purpose is...um...to not do anything，That is, to replace other context managers without changing the code structure。
    Context managers are a type of Python object，Used in conjunction with the with statement，
    To ensure that some resources are properly initialized and cleaned up during code block execution。
    Context managers must implement two methods，They are __enter__()and __exit__()。
    At the beginning of the context execution，__enter__()The method is called before the code block is executed，
    While at the end of the context execution，__exit__()The method is called。
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return


def run_gradio_in_subpath(demo, auth, port, custom_path):
    """
    Change the running address of Gradio to the specified secondary path
    """

    def is_path_legal(path: str) -> bool:
        """
        check path for sub url
        path: path to check
        return value: do sub url wrap
        """
        if path == "/":
            return True
        if len(path) == 0:
            print(
                "ilegal custom path: {}\npath must not be empty\ndeploy on root url".format(
                    path
                )
            )
            return False
        if path[0] == "/":
            if path[1] != "/":
                print("deploy on sub-path {}".format(path))
                return True
            return False
        print(
            "ilegal custom path: {}\npath should begin with '/'\ndeploy on root url".format(
                path
            )
        )
        return False

    if not is_path_legal(custom_path):
        raise RuntimeError("Ilegal custom path")
    import uvicorn
    import fake_gradio as gr
    from fastapi import FastAPI

    app = FastAPI()
    if custom_path != "/":

        @app.get("/")
        def read_main():
            return {"message": f"Gradio is running at: {custom_path}"}

    app = gr.mount_gradio_app(app, demo, path=custom_path)
    uvicorn.run(app, host="0.0.0.0", port=port)  # , auth=auth


def clip_history(inputs, history, tokenizer, max_token_limit):
    """
    reduce the length of history by clipping.
    this function search for the longest entries to clip, little by little,
    until the number of token of history is reduced under threshold.
    Shorten the length of the history by trimming。
    This function gradually searches for the longest entry to clip，
    Until the number of history markers is reduced to below the threshold。
    """
    import numpy as np
    from void_terminal.request_llms.bridge_all import model_info

    def get_token_num(txt):
        return len(tokenizer.encode(txt, disallowed_special=()))

    input_token_num = get_token_num(inputs)

    if max_token_limit < 5000:
        output_token_expect = 256  # 4k & 2k models
    elif max_token_limit < 9000:
        output_token_expect = 512  # 8k models
    else:
        output_token_expect = 1024  # 16k & 32k models

    if input_token_num < max_token_limit * 3 / 4:
        # When the token proportion of the input part is less than 3/4 of the limit，When trimming
        # 1. Leave the surplus of input
        max_token_limit = max_token_limit - input_token_num
        # 2. Leave the surplus used for output
        max_token_limit = max_token_limit - output_token_expect
        # 3. If the surplus is too small，Clear the history directly
        if max_token_limit < output_token_expect:
            history = []
            return history
    else:
        # When the token proportion of the input part > is 3/4 of the limit，Clear the history directly
        history = []
        return history

    everything = [""]
    everything.extend(history)
    n_token = get_token_num("\n".join(everything))
    everything_token = [get_token_num(e) for e in everything]

    # Granularity when truncating
    delta = max(everything_token) // 16

    while n_token > max_token_limit:
        where = np.argmax(everything_token)
        encoded = tokenizer.encode(everything[where], disallowed_special=())
        clipped_encoded = encoded[: len(encoded) - delta]
        everything[where] = tokenizer.decode(clipped_encoded)[
            :-1
        ]  # -1 to remove the may-be illegal char
        everything_token[where] = get_token_num(everything[where])
        n_token = get_token_num("\n".join(everything))

    history = everything[1:]
    return history


"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
Part III
Other utilities:
    - zip_folder:    Compress all files under a certain path，Then move to a specified path（Written by GPT）
    - gen_time_str:  Generate a timestamp
    - ProxyNetworkActivate: Temporarily start proxy network（If there is）
    - objdump/objload: Convenient debugging function
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


def zip_folder(source_folder, dest_folder, zip_name):
    import zipfile
    import os

    # Make sure the source folder exists
    if not os.path.exists(source_folder):
        print(f"{source_folder} does not exist")
        return

    # Make sure the destination folder exists
    if not os.path.exists(dest_folder):
        print(f"{dest_folder} does not exist")
        return

    # Create the name for the zip file
    zip_file = pj(dest_folder, zip_name)

    # Create a ZipFile object
    with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the source folder and add files to the zip file
        for foldername, subfolders, filenames in os.walk(source_folder):
            for filename in filenames:
                filepath = pj(foldername, filename)
                zipf.write(filepath, arcname=os.path.relpath(filepath, source_folder))

    # Move the zip file to the destination folder (if it wasn't already there)
    if os.path.dirname(zip_file) != dest_folder:
        os.rename(zip_file, pj(dest_folder, os.path.basename(zip_file)))
        zip_file = pj(dest_folder, os.path.basename(zip_file))

    print(f"Zip file created at {zip_file}")


def zip_result(folder):
    t = gen_time_str()
    zip_folder(folder, get_log_folder(), f"{t}-result.zip")
    return pj(get_log_folder(), f"{t}-result.zip")


def gen_time_str():
    import time

    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())


def get_log_folder(user=default_user_name, plugin_name="shared"):
    if user is None:
        user = default_user_name
    PATH_LOGGING = get_conf("PATH_LOGGING")
    if plugin_name is None:
        _dir = pj(PATH_LOGGING, user)
    else:
        _dir = pj(PATH_LOGGING, user, plugin_name)
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    return _dir


def get_upload_folder(user=default_user_name, tag=None):
    PATH_PRIVATE_UPLOAD = get_conf("PATH_PRIVATE_UPLOAD")
    if user is None:
        user = default_user_name
    if tag is None or len(tag) == 0:
        target_path_base = pj(PATH_PRIVATE_UPLOAD, user)
    else:
        target_path_base = pj(PATH_PRIVATE_UPLOAD, user, tag)
    return target_path_base


def is_the_upload_folder(string):
    PATH_PRIVATE_UPLOAD = get_conf("PATH_PRIVATE_UPLOAD")
    pattern = r"^PATH_PRIVATE_UPLOAD[\\/][A-Za-z0-9_-]+[\\/]\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}$"
    pattern = pattern.replace("PATH_PRIVATE_UPLOAD", PATH_PRIVATE_UPLOAD)
    if re.match(pattern, string):
        return True
    else:
        return False


def get_user(chatbotwithcookies:ChatBotWithCookies):
    return chatbotwithcookies._cookies.get("user_name", default_user_name)


class ProxyNetworkActivate:
    """
    This code defines an empty context manager named ProxyNetworkActivate, Used to proxy a small piece of code
    """

    def __init__(self, task=None) -> None:
        self.task = task
        if not task:
            # No task given, Then we default to proxy
            self.valid = True
        else:
            # Given a task, Let`s check
            from void_terminal.toolbox import get_conf

            WHEN_TO_USE_PROXY = get_conf("WHEN_TO_USE_PROXY")
            self.valid = task in WHEN_TO_USE_PROXY

    def __enter__(self):
        if not self.valid:
            return self
        from void_terminal.toolbox import get_conf

        proxies = get_conf("proxies")
        if "no_proxy" in os.environ:
            os.environ.pop("no_proxy")
        if proxies is not None:
            if "http" in proxies:
                os.environ["HTTP_PROXY"] = proxies["http"]
            if "https" in proxies:
                os.environ["HTTPS_PROXY"] = proxies["https"]
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        os.environ["no_proxy"] = "*"
        if "HTTP_PROXY" in os.environ:
            os.environ.pop("HTTP_PROXY")
        if "HTTPS_PROXY" in os.environ:
            os.environ.pop("HTTPS_PROXY")
        return


def Singleton(cls):
    """
    Single instance decorator
    """
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


def get_pictures_list(path):
    file_manifest = [f for f in glob.glob(f"{path}/**/*.jpg", recursive=True)]
    file_manifest += [f for f in glob.glob(f"{path}/**/*.jpeg", recursive=True)]
    file_manifest += [f for f in glob.glob(f"{path}/**/*.png", recursive=True)]
    return file_manifest


def have_any_recent_upload_image_files(chatbot:ChatBotWithCookies):
    _5min = 5 * 60
    if chatbot is None:
        return False, None  # chatbot is None
    most_recent_uploaded = chatbot._cookies.get("most_recent_uploaded", None)
    if not most_recent_uploaded:
        return False, None  # most_recent_uploaded is None
    if time.time() - most_recent_uploaded["time"] < _5min:
        most_recent_uploaded = chatbot._cookies.get("most_recent_uploaded", None)
        path = most_recent_uploaded["path"]
        file_manifest = get_pictures_list(path)
        if len(file_manifest) == 0:
            return False, None
        return True, file_manifest  # most_recent_uploaded is new
    else:
        return False, None  # most_recent_uploaded is too old

# Claude3 model supports graphic context dialogue, reads all images
def every_image_file_in_path(chatbot:ChatBotWithCookies):
    if chatbot is None:
        return False, []  # chatbot is None
    most_recent_uploaded = chatbot._cookies.get("most_recent_uploaded", None)
    if not most_recent_uploaded:
        return False, []  # most_recent_uploaded is None
    path = most_recent_uploaded["path"]
    file_manifest = get_pictures_list(path)
    if len(file_manifest) == 0:
        return False, []
    return True, file_manifest

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_max_token(llm_kwargs):
    from void_terminal.request_llms.bridge_all import model_info

    return model_info[llm_kwargs["llm_model"]]["max_token"]


def check_packages(packages=[]):
    import importlib.util

    for p in packages:
        spam_spec = importlib.util.find_spec(p)
        if spam_spec is None:
            raise ModuleNotFoundError


def map_file_to_sha256(file_path):
    import hashlib

    with open(file_path, 'rb') as file:
        content = file.read()

    # Calculate the SHA-256 hash of the file contents
    sha_hash = hashlib.sha256(content).hexdigest()

    return sha_hash


def check_repeat_upload(new_pdf_path, pdf_hash):
    '''
    Check if the previously uploaded file is the same as the newly uploaded file，If the same, return(True, Duplicate file path)，Otherwise return(False，None)
    '''
    from void_terminal.toolbox import get_conf
    import PyPDF2

    user_upload_dir = os.path.dirname(os.path.dirname(new_pdf_path))
    file_name = os.path.basename(new_pdf_path)

    file_manifest = [f for f in glob.glob(f'{user_upload_dir}/**/{file_name}', recursive=True)]

    for saved_file in file_manifest:
        with open(new_pdf_path, 'rb') as file1, open(saved_file, 'rb') as file2:
            reader1 = PyPDF2.PdfFileReader(file1)
            reader2 = PyPDF2.PdfFileReader(file2)

            # Compare if the number of pages is the same
            if reader1.getNumPages() != reader2.getNumPages():
                continue

            # Compare whether each page`s content is the same
            for page_num in range(reader1.getNumPages()):
                page1 = reader1.getPage(page_num).extractText()
                page2 = reader2.getPage(page_num).extractText()
                if page1 != page2:
                    continue

        maybe_project_dir = glob.glob('{}/**/{}'.format(get_log_folder(), pdf_hash + ".tag"), recursive=True)


        if len(maybe_project_dir) > 0:
            return True, os.path.dirname(maybe_project_dir[0])

    # If all pages have the same content，Return True
    return False, None

def log_chat(llm_model: str, input_str: str, output_str: str):
    try:
        if output_str and input_str and llm_model:
            uid = str(uuid.uuid4().hex)
            logging.info(f"[Model({uid})] {llm_model}")
            input_str = input_str.rstrip('\n')
            logging.info(f"[Query({uid})]\n{input_str}")
            output_str = output_str.rstrip('\n')
            logging.info(f"[Response({uid})]\n{output_str}\n\n")
    except:
        print(trimmed_format_exc())
