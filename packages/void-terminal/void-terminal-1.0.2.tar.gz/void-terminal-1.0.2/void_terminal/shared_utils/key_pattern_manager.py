import re
import os
from functools import wraps, lru_cache
from void_terminal.shared_utils.advanced_markdown_format import format_io
from void_terminal.shared_utils.config_loader import get_conf as get_conf


pj = os.path.join
default_user_name = 'default_user'


def is_openai_api_key(key):
    CUSTOM_API_KEY_PATTERN = get_conf('CUSTOM_API_KEY_PATTERN')
    if len(CUSTOM_API_KEY_PATTERN) != 0:
        API_MATCH_ORIGINAL = re.match(CUSTOM_API_KEY_PATTERN, key)
    else:
        API_MATCH_ORIGINAL = re.match(r"sk-[a-zA-Z0-9]{48}$|sk-proj-[a-zA-Z0-9]{48}$|sess-[a-zA-Z0-9]{40}$", key)
    return bool(API_MATCH_ORIGINAL)


def is_azure_api_key(key):
    API_MATCH_AZURE = re.match(r"[a-zA-Z0-9]{32}$", key)
    return bool(API_MATCH_AZURE)


def is_api2d_key(key):
    API_MATCH_API2D = re.match(r"fk[a-zA-Z0-9]{6}-[a-zA-Z0-9]{32}$", key)
    return bool(API_MATCH_API2D)


def is_cohere_api_key(key):
    API_MATCH_AZURE = re.match(r"[a-zA-Z0-9]{40}$", key)
    return bool(API_MATCH_AZURE)


def is_any_api_key(key):
    if ',' in key:
        keys = key.split(',')
        for k in keys:
            if is_any_api_key(k): return True
        return False
    else:
        return is_openai_api_key(key) or is_api2d_key(key) or is_azure_api_key(key) or is_cohere_api_key(key)


def what_keys(keys):
    avail_key_list = {'OpenAI Key': 0, "Azure Key": 0, "API2D Key": 0}
    key_list = keys.split(',')

    for k in key_list:
        if is_openai_api_key(k):
            avail_key_list['OpenAI Key'] += 1

    for k in key_list:
        if is_api2d_key(k):
            avail_key_list['API2D Key'] += 1

    for k in key_list:
        if is_azure_api_key(k):
            avail_key_list['Azure Key'] += 1

    return f"Detected： OpenAI Key {avail_key_list['OpenAI Key']} items, Azure Key {avail_key_list['Azure Key']} items, API2D Key {avail_key_list['API2D Key']} items"


def select_api_key(keys, llm_model):
    import random
    avail_key_list = []
    key_list = keys.split(',')

    if llm_model.startswith('gpt-') or llm_model.startswith('one-api-'):
        for k in key_list:
            if is_openai_api_key(k): avail_key_list.append(k)

    if llm_model.startswith('api2d-'):
        for k in key_list:
            if is_api2d_key(k): avail_key_list.append(k)

    if llm_model.startswith('azure-'):
        for k in key_list:
            if is_azure_api_key(k): avail_key_list.append(k)

    if llm_model.startswith('cohere-'):
        for k in key_list:
            if is_cohere_api_key(k): avail_key_list.append(k)

    if len(avail_key_list) == 0:
        raise RuntimeError(f"The api-key you provided does not meet the requirements，Does not contain any that can be used for{llm_model}api-key。You may have selected the wrong model or request source（Switch to OpenAI in the model change menu in the top left corner,azure,claude,Cohere and other request sources）。")

    api_key = random.choice(avail_key_list) # Random load balancing
    return api_key
