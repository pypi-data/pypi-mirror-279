import importlib
import time
import os
from functools import lru_cache
from void_terminal.shared_utils.colorful import PrintBrightRed, PrintBrightGreen, PrintBrightBlue

pj = os.path.join
default_user_name = 'default_user'

def read_env_variable(arg, default_value):
    """
    Environment variables can be `GPT_ACADEMIC_CONFIG`(preferred)，or can be directly`CONFIG`
    For example, in windows cmd，it can be written as：
        set USE_PROXY=True
        set API_KEY=sk-j7caBpkRoxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        set proxies={"http":"http://127.0.0.1:10085", "https":"http://127.0.0.1:10085",}
        set AVAIL_LLM_MODELS=["gpt-3.5-turbo", "chatglm"]
        set AUTHENTICATION=[("username", "password"), ("username2", "password2")]
    or as：
        set GPT_ACADEMIC_USE_PROXY=True
        set GPT_ACADEMIC_API_KEY=sk-j7caBpkRoxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        set GPT_ACADEMIC_proxies={"http":"http://127.0.0.1:10085", "https":"http://127.0.0.1:10085",}
        set GPT_ACADEMIC_AVAIL_LLM_MODELS=["gpt-3.5-turbo", "chatglm"]
        set GPT_ACADEMIC_AUTHENTICATION=[("username", "password"), ("username2", "password2")]
    """
    arg_with_prefix = "GPT_ACADEMIC_" + arg
    if arg_with_prefix in os.environ:
        env_arg = os.environ[arg_with_prefix]
    elif arg in os.environ:
        env_arg = os.environ[arg]
    else:
        raise KeyError
    print(f"[ENV_VAR] Attempting to load{arg}，Default value：{default_value} --> Corrected value：{env_arg}")
    try:
        if isinstance(default_value, bool):
            env_arg = env_arg.strip()
            if env_arg == 'True': r = True
            elif env_arg == 'False': r = False
            else: print('Enter True or False, but have:', env_arg); r = default_value
        elif isinstance(default_value, int):
            r = int(env_arg)
        elif isinstance(default_value, float):
            r = float(env_arg)
        elif isinstance(default_value, str):
            r = env_arg.strip()
        elif isinstance(default_value, dict):
            r = eval(env_arg)
        elif isinstance(default_value, list):
            r = eval(env_arg)
        elif default_value is None:
            assert arg == "proxies"
            r = eval(env_arg)
        else:
            PrintBrightRed(f"[ENV_VAR] Environment variable{arg}Setting through environment variables is not supported! ")
            raise KeyError
    except:
        PrintBrightRed(f"[ENV_VAR] Environment variable{arg}Loading failed! ")
        raise KeyError(f"[ENV_VAR] Environment variable{arg}Loading failed! ")

    PrintBrightGreen(f"[ENV_VAR] Successfully read environment variable: {arg}")
    return r


@lru_cache(maxsize=128)
def read_single_conf_with_lru_cache(arg):
    from void_terminal.shared_utils.key_pattern_manager import is_any_api_key
    try:
        # Priority 1. Get environment variables as configuration
        default_ref = getattr(importlib.import_module('void_terminal.config'), arg) # Read the default value as a reference for data type conversion
        r = read_env_variable(arg, default_ref)
    except:
        try:
            # Priority 2. Get the configuration in config_private
            r = getattr(importlib.import_module('void_terminal.config_private'), arg)
        except:
            # Priority 3. Get the configuration in config
            r = getattr(importlib.import_module('void_terminal.config'), arg)

    # When reading API_KEY，Check if you forgot to change the config
    if arg == 'API_URL_REDIRECT':
        oai_rd = r.get("https://api.openai.com/v1/chat/completions", None) # The format of API_URL_REDIRECT is incorrect，Please read`https://github.com/binary-husky/gpt_academic/wiki/项目配置Say明`
        if oai_rd and not oai_rd.endswith('/completions'):
            PrintBrightRed("\n\n[API_URL_REDIRECT] API_URL_REDIRECT is filled incorrectly。Please read`https://github.com/binary-husky/gpt_academic/wiki/项目配置Say明`。If you are sure you haven`t made a mistake，You can ignore this message。")
            time.sleep(5)
    if arg == 'API_KEY':
        PrintBrightBlue(f"[API_KEY] This project now supports OpenAI and Azure`s api-key。It also supports filling in multiple api-keys at the same time， e.g., API_KEY=\"openai-key1,openai-key2,azure-key3\"")
        PrintBrightBlue(f"[API_KEY] You can modify the api-key in config.py(s)，You can also enter a temporary api-key in the question input area(s)，After submitting with the enter key, it will take effect。")
        if is_any_api_key(r):
            PrintBrightGreen(f"[API_KEY] Your API_KEY is: {r[:15]}*** API_KEY imported successfully")
        else:
            PrintBrightRed("[API_KEY] Your API_KEY does not meet any known key format，Please modify the API key in the config file before running。")
    if arg == 'proxies':
        if not read_single_conf_with_lru_cache('USE_PROXY'): r = None # Check USE_PROXY，Prevent proxies from working alone
        if r is None:
            PrintBrightRed('[PROXY] Network proxy status：Not configured。。Suggestion：Check if the USE_PROXY option has been modified。')
        else:
            PrintBrightGreen('[PROXY] Network proxy status：Configured。Configuration information is as follows：', r)
            assert isinstance(r, dict), 'Proxies format error，Please note the format of the proxies option，Do not miss the parentheses。'
    return r


@lru_cache(maxsize=128)
def get_conf(*args):
    """
    All configurations for this project are centralized in config.py。 There are three ways to modify the configuration，You only need to choose one of them：
        - Directly modify config.py
        - Create and modify config_private.py
        - Modify environment variables（Modifying docker-compose.yml is Equivalent to Modifying the Internal Environment Variables of the Container）

    Attention：If you deploy using docker-compose，Please modify docker-compose（Equivalent to modifying the environment variables inside the container）
    """
    res = []
    for arg in args:
        r = read_single_conf_with_lru_cache(arg)
        res.append(r)
    if len(res) == 1: return res[0]
    return res


def set_conf(key, value):
    from void_terminal.toolbox import read_single_conf_with_lru_cache
    read_single_conf_with_lru_cache.cache_clear()
    get_conf.cache_clear()
    os.environ[key] = str(value)
    altered = get_conf(key)
    return altered


def set_multi_conf(dic):
    for k, v in dic.items(): set_conf(k, v)
    return
