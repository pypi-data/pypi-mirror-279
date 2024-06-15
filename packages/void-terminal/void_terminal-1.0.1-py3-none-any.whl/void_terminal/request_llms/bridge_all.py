
"""
    There are mainly 2 functions in this file，It is a common interface for all LLMs，They will continue to call lower-level LLM models，Handling details such as multi-model parallelism

    Functions without multi-threading capability：Used in normal conversation，Fully interactive，Not multi-threaded
    1. predict(...)

    Functions with multi-threading capability：Called in function plugins，Flexible and concise
    2. predict_no_ui_long_connection(...)
"""
import tiktoken, copy, re
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
from void_terminal.toolbox import get_conf, trimmed_format_exc, apply_gpt_academic_string_mask, read_one_api_model_name

from void_terminal.request_llms.bridge_chatgpt import predict_no_ui_long_connection as chatgpt_noui
from void_terminal.request_llms.bridge_chatgpt import predict as chatgpt_ui

from void_terminal.request_llms.bridge_chatgpt_vision import predict_no_ui_long_connection as chatgpt_vision_noui
from void_terminal.request_llms.bridge_chatgpt_vision import predict as chatgpt_vision_ui

from void_terminal.request_llms.bridge_chatglm import predict_no_ui_long_connection as chatglm_noui
from void_terminal.request_llms.bridge_chatglm import predict as chatglm_ui

from void_terminal.request_llms.bridge_chatglm3 import predict_no_ui_long_connection as chatglm3_noui
from void_terminal.request_llms.bridge_chatglm3 import predict as chatglm3_ui

from void_terminal.request_llms.bridge_qianfan import predict_no_ui_long_connection as qianfan_noui
from void_terminal.request_llms.bridge_qianfan import predict as qianfan_ui

from void_terminal.request_llms.bridge_google_gemini import predict as genai_ui
from void_terminal.request_llms.bridge_google_gemini import predict_no_ui_long_connection  as genai_noui

from void_terminal.request_llms.bridge_zhipu import predict_no_ui_long_connection as zhipu_noui
from void_terminal.request_llms.bridge_zhipu import predict as zhipu_ui

from void_terminal.request_llms.bridge_cohere import predict as cohere_ui
from void_terminal.request_llms.bridge_cohere import predict_no_ui_long_connection as cohere_noui

from void_terminal.request_llms.oai_std_model_template import get_predict_function

colors = ['#FF00FF', '#00FFFF', '#FF0000', '#990099', '#009999', '#990044']

class LazyloadTiktoken(object):
    def __init__(self, model):
        self.model = model

    @staticmethod
    @lru_cache(maxsize=128)
    def get_encoder(model):
        print('Loading tokenizer，If it is the first time running，It may take some time to download parameters')
        tmp = tiktoken.encoding_for_model(model)
        print('Loading tokenizer completed')
        return tmp

    def encode(self, *args, **kwargs):
        encoder = self.get_encoder(self.model)
        return encoder.encode(*args, **kwargs)

    def decode(self, *args, **kwargs):
        encoder = self.get_encoder(self.model)
        return encoder.decode(*args, **kwargs)

# Endpoint redirection
API_URL_REDIRECT, AZURE_ENDPOINT, AZURE_ENGINE = get_conf("API_URL_REDIRECT", "AZURE_ENDPOINT", "AZURE_ENGINE")
openai_endpoint = "https://api.openai.com/v1/chat/completions"
api2d_endpoint = "https://openai.api2d.net/v1/chat/completions"
newbing_endpoint = "wss://sydney.bing.com/sydney/ChatHub"
gemini_endpoint = "https://generativelanguage.googleapis.com/v1beta/models"
claude_endpoint = "https://api.anthropic.com/v1/messages"
cohere_endpoint = "https://api.cohere.ai/v1/chat"
ollama_endpoint = "http://localhost:11434/api/chat"
yimodel_endpoint = "https://api.lingyiwanwu.com/v1/chat/completions"
deepseekapi_endpoint = "https://api.deepseek.com/v1/chat/completions"

if not AZURE_ENDPOINT.endswith('/'): AZURE_ENDPOINT += '/'
azure_endpoint = AZURE_ENDPOINT + f'openai/deployments/{AZURE_ENGINE}/chat/completions?api-version=2023-05-15'
# Compatible with old version configuration
try:
    API_URL = get_conf("API_URL")
    if API_URL != "https://api.openai.com/v1/chat/completions":
        openai_endpoint = API_URL
        print("Warning! The API_URL configuration option will be deprecated，Please replace it with the API_URL_REDIRECT configuration")
except:
    pass
# New version configuration
if openai_endpoint in API_URL_REDIRECT: openai_endpoint = API_URL_REDIRECT[openai_endpoint]
if api2d_endpoint in API_URL_REDIRECT: api2d_endpoint = API_URL_REDIRECT[api2d_endpoint]
if newbing_endpoint in API_URL_REDIRECT: newbing_endpoint = API_URL_REDIRECT[newbing_endpoint]
if gemini_endpoint in API_URL_REDIRECT: gemini_endpoint = API_URL_REDIRECT[gemini_endpoint]
if claude_endpoint in API_URL_REDIRECT: claude_endpoint = API_URL_REDIRECT[claude_endpoint]
if cohere_endpoint in API_URL_REDIRECT: cohere_endpoint = API_URL_REDIRECT[cohere_endpoint]
if ollama_endpoint in API_URL_REDIRECT: ollama_endpoint = API_URL_REDIRECT[ollama_endpoint]
if yimodel_endpoint in API_URL_REDIRECT: yimodel_endpoint = API_URL_REDIRECT[yimodel_endpoint]
if deepseekapi_endpoint in API_URL_REDIRECT: deepseekapi_endpoint = API_URL_REDIRECT[deepseekapi_endpoint]

# Get tokenizer
tokenizer_gpt35 = LazyloadTiktoken("gpt-3.5-turbo")
tokenizer_gpt4 = LazyloadTiktoken("gpt-4")
get_token_num_gpt35 = lambda txt: len(tokenizer_gpt35.encode(txt, disallowed_special=()))
get_token_num_gpt4 = lambda txt: len(tokenizer_gpt4.encode(txt, disallowed_special=()))


# Start initializing model
AVAIL_LLM_MODELS, LLM_MODEL = get_conf("AVAIL_LLM_MODELS", "LLM_MODEL")
AVAIL_LLM_MODELS = AVAIL_LLM_MODELS + [LLM_MODEL]
# -=-=-=-=-=-=- The following section is the earliest and most stable model added
model_info = {
    # openai
    "gpt-3.5-turbo": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 16385,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "gpt-3.5-turbo-16k": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 16385,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "gpt-3.5-turbo-0613": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 4096,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "gpt-3.5-turbo-16k-0613": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 16385,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "gpt-3.5-turbo-1106": { #16k
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 16385,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "gpt-3.5-turbo-0125": { #16k
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 16385,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "gpt-4": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 8192,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4-32k": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 32768,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4o": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4o-2024-05-13": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4-turbo-preview": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4-1106-preview": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4-0125-preview": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4-turbo": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4-turbo-2024-04-09": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 128000,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },


    "gpt-3.5-random": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": openai_endpoint,
        "max_token": 4096,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    "gpt-4-vision-preview": {
        "fn_with_ui": chatgpt_vision_ui,
        "fn_without_ui": chatgpt_vision_noui,
        "endpoint": openai_endpoint,
        "max_token": 4096,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },


    # azure openai
    "azure-gpt-3.5":{
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": azure_endpoint,
        "max_token": 4096,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    "azure-gpt-4":{
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": azure_endpoint,
        "max_token": 8192,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    # Zhipu AI
    "glm-4": {
        "fn_with_ui": zhipu_ui,
        "fn_without_ui": zhipu_noui,
        "endpoint": None,
        "max_token": 10124 * 8,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "glm-4-0520": {
        "fn_with_ui": zhipu_ui,
        "fn_without_ui": zhipu_noui,
        "endpoint": None,
        "max_token": 10124 * 8,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "glm-4-air": {
        "fn_with_ui": zhipu_ui,
        "fn_without_ui": zhipu_noui,
        "endpoint": None,
        "max_token": 10124 * 8,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "glm-4-airx": {
        "fn_with_ui": zhipu_ui,
        "fn_without_ui": zhipu_noui,
        "endpoint": None,
        "max_token": 10124 * 8,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "glm-4-flash": {
         "fn_with_ui": zhipu_ui,
        "fn_without_ui": zhipu_noui,
        "endpoint": None,
        "max_token": 10124 * 8,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,       
    },
    "glm-4v": {
        "fn_with_ui": zhipu_ui,
        "fn_without_ui": zhipu_noui,
        "endpoint": None,
        "max_token": 1000,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "glm-3-turbo": {
        "fn_with_ui": zhipu_ui,
        "fn_without_ui": zhipu_noui,
        "endpoint": None,
        "max_token": 10124 * 4,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    # api_2d (No need to add the api2d interface here anymore，Because the following code will be automatically added)
    "api2d-gpt-4": {
        "fn_with_ui": chatgpt_ui,
        "fn_without_ui": chatgpt_noui,
        "endpoint": api2d_endpoint,
        "max_token": 8192,
        "tokenizer": tokenizer_gpt4,
        "token_cnt": get_token_num_gpt4,
    },

    # Align chatglm directly to chatglm2
    "chatglm": {
        "fn_with_ui": chatglm_ui,
        "fn_without_ui": chatglm_noui,
        "endpoint": None,
        "max_token": 1024,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "chatglm2": {
        "fn_with_ui": chatglm_ui,
        "fn_without_ui": chatglm_noui,
        "endpoint": None,
        "max_token": 1024,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "chatglm3": {
        "fn_with_ui": chatglm3_ui,
        "fn_without_ui": chatglm3_noui,
        "endpoint": None,
        "max_token": 8192,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "qianfan": {
        "fn_with_ui": qianfan_ui,
        "fn_without_ui": qianfan_noui,
        "endpoint": None,
        "max_token": 2000,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "gemini-pro": {
        "fn_with_ui": genai_ui,
        "fn_without_ui": genai_noui,
        "endpoint": gemini_endpoint,
        "max_token": 1024 * 32,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "gemini-pro-vision": {
        "fn_with_ui": genai_ui,
        "fn_without_ui": genai_noui,
        "endpoint": gemini_endpoint,
        "max_token": 1024 * 32,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

    # cohere
    "cohere-command-r-plus": {
        "fn_with_ui": cohere_ui,
        "fn_without_ui": cohere_noui,
        "can_multi_thread": True,
        "endpoint": cohere_endpoint,
        "max_token": 1024 * 4,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },

}
# -=-=-=-=-=-=- The Dark Side of the Moon -=-=-=-=-=-=-
from void_terminal.request_llms.bridge_moonshot import predict as moonshot_ui
from void_terminal.request_llms.bridge_moonshot import predict_no_ui_long_connection as moonshot_no_ui
model_info.update({
    "moonshot-v1-8k": {
        "fn_with_ui": moonshot_ui,
        "fn_without_ui": moonshot_no_ui,
        "can_multi_thread": True,
        "endpoint": None,
        "max_token": 1024 * 8,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "moonshot-v1-32k": {
        "fn_with_ui": moonshot_ui,
        "fn_without_ui": moonshot_no_ui,
        "can_multi_thread": True,
        "endpoint": None,
        "max_token": 1024 * 32,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    },
    "moonshot-v1-128k": {
        "fn_with_ui": moonshot_ui,
        "fn_without_ui": moonshot_no_ui,
        "can_multi_thread": True,
        "endpoint": None,
        "max_token": 1024 * 128,
        "tokenizer": tokenizer_gpt35,
        "token_cnt": get_token_num_gpt35,
    }
})
# -=-=-=-=-=-=- api2d alignment support -=-=-=-=-=-=-
for model in AVAIL_LLM_MODELS:
    if model.startswith('api2d-') and (model.replace('api2d-','') in model_info.keys()):
        mi = copy.deepcopy(model_info[model.replace('api2d-','')])
        mi.update({"endpoint": api2d_endpoint})
        model_info.update({model: mi})

# -=-=-=-=-=-=- Azure alignment support -=-=-=-=-=-=-
for model in AVAIL_LLM_MODELS:
    if model.startswith('azure-') and (model.replace('azure-','') in model_info.keys()):
        mi = copy.deepcopy(model_info[model.replace('azure-','')])
        mi.update({"endpoint": azure_endpoint})
        model_info.update({model: mi})

# -=-=-=-=-=-=- The following section is the newly added model，May come with additional dependencies -=-=-=-=-=-=-
# Claude Family
claude_models = ["claude-instant-1.2","claude-2.0","claude-2.1","claude-3-haiku-20240307","claude-3-sonnet-20240229","claude-3-opus-20240229"]
if any(item in claude_models for item in AVAIL_LLM_MODELS):
    from void_terminal.request_llms.bridge_claude import predict_no_ui_long_connection as claude_noui
    from void_terminal.request_llms.bridge_claude import predict as claude_ui
    model_info.update({
        "claude-instant-1.2": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": claude_endpoint,
            "max_token": 100000,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
    model_info.update({
        "claude-2.0": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": claude_endpoint,
            "max_token": 100000,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
    model_info.update({
        "claude-2.1": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": claude_endpoint,
            "max_token": 200000,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
    model_info.update({
        "claude-3-haiku-20240307": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": claude_endpoint,
            "max_token": 200000,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
    model_info.update({
        "claude-3-sonnet-20240229": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": claude_endpoint,
            "max_token": 200000,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
    model_info.update({
        "claude-3-opus-20240229": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": claude_endpoint,
            "max_token": 200000,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
if "jittorllms_rwkv" in AVAIL_LLM_MODELS:
    from void_terminal.request_llms.bridge_jittorllms_rwkv import predict_no_ui_long_connection as rwkv_noui
    from void_terminal.request_llms.bridge_jittorllms_rwkv import predict as rwkv_ui
    model_info.update({
        "jittorllms_rwkv": {
            "fn_with_ui": rwkv_ui,
            "fn_without_ui": rwkv_noui,
            "endpoint": None,
            "max_token": 1024,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
if "jittorllms_llama" in AVAIL_LLM_MODELS:
    from void_terminal.request_llms.bridge_jittorllms_llama import predict_no_ui_long_connection as llama_noui
    from void_terminal.request_llms.bridge_jittorllms_llama import predict as llama_ui
    model_info.update({
        "jittorllms_llama": {
            "fn_with_ui": llama_ui,
            "fn_without_ui": llama_noui,
            "endpoint": None,
            "max_token": 1024,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
if "jittorllms_pangualpha" in AVAIL_LLM_MODELS:
    from void_terminal.request_llms.bridge_jittorllms_pangualpha import predict_no_ui_long_connection as pangualpha_noui
    from void_terminal.request_llms.bridge_jittorllms_pangualpha import predict as pangualpha_ui
    model_info.update({
        "jittorllms_pangualpha": {
            "fn_with_ui": pangualpha_ui,
            "fn_without_ui": pangualpha_noui,
            "endpoint": None,
            "max_token": 1024,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
if "moss" in AVAIL_LLM_MODELS:
    from void_terminal.request_llms.bridge_moss import predict_no_ui_long_connection as moss_noui
    from void_terminal.request_llms.bridge_moss import predict as moss_ui
    model_info.update({
        "moss": {
            "fn_with_ui": moss_ui,
            "fn_without_ui": moss_noui,
            "endpoint": None,
            "max_token": 1024,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
if "stack-claude" in AVAIL_LLM_MODELS:
    from void_terminal.request_llms.bridge_stackclaude import predict_no_ui_long_connection as claude_noui
    from void_terminal.request_llms.bridge_stackclaude import predict as claude_ui
    model_info.update({
        "stack-claude": {
            "fn_with_ui": claude_ui,
            "fn_without_ui": claude_noui,
            "endpoint": None,
            "max_token": 8192,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        }
    })
if "newbing" in AVAIL_LLM_MODELS:   # same with newbing-free
    try:
        from void_terminal.request_llms.bridge_newbingfree import predict_no_ui_long_connection as newbingfree_noui
        from void_terminal.request_llms.bridge_newbingfree import predict as newbingfree_ui
        model_info.update({
            "newbing": {
                "fn_with_ui": newbingfree_ui,
                "fn_without_ui": newbingfree_noui,
                "endpoint": newbing_endpoint,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
if "chatglmft" in AVAIL_LLM_MODELS:   # same with newbing-free
    try:
        from void_terminal.request_llms.bridge_chatglmft import predict_no_ui_long_connection as chatglmft_noui
        from void_terminal.request_llms.bridge_chatglmft import predict as chatglmft_ui
        model_info.update({
            "chatglmft": {
                "fn_with_ui": chatglmft_ui,
                "fn_without_ui": chatglmft_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
# -=-=-=-=-=-=- Shanghai AI-LAB Shu Sheng Large Model -=-=-=-=-=-=-
if "internlm" in AVAIL_LLM_MODELS:
    try:
        from void_terminal.request_llms.bridge_internlm import predict_no_ui_long_connection as internlm_noui
        from void_terminal.request_llms.bridge_internlm import predict as internlm_ui
        model_info.update({
            "internlm": {
                "fn_with_ui": internlm_ui,
                "fn_without_ui": internlm_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
if "chatglm_onnx" in AVAIL_LLM_MODELS:
    try:
        from void_terminal.request_llms.bridge_chatglmonnx import predict_no_ui_long_connection as chatglm_onnx_noui
        from void_terminal.request_llms.bridge_chatglmonnx import predict as chatglm_onnx_ui
        model_info.update({
            "chatglm_onnx": {
                "fn_with_ui": chatglm_onnx_ui,
                "fn_without_ui": chatglm_onnx_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
# -=-=-=-=-=-=- Tongyi - Local Model
if "qwen-local" in AVAIL_LLM_MODELS:
    try:
        from void_terminal.request_llms.bridge_qwen_local import predict_no_ui_long_connection as qwen_local_noui
        from void_terminal.request_llms.bridge_qwen_local import predict as qwen_local_ui
        model_info.update({
            "qwen-local": {
                "fn_with_ui": qwen_local_ui,
                "fn_without_ui": qwen_local_noui,
                "can_multi_thread": False,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
# -=-=-=-=-=-=- Tongyi - Online Model
if "qwen-turbo" in AVAIL_LLM_MODELS or "qwen-plus" in AVAIL_LLM_MODELS or "qwen-max" in AVAIL_LLM_MODELS:   # zhipuai
    try:
        from void_terminal.request_llms.bridge_qwen import predict_no_ui_long_connection as qwen_noui
        from void_terminal.request_llms.bridge_qwen import predict as qwen_ui
        model_info.update({
            "qwen-turbo": {
                "fn_with_ui": qwen_ui,
                "fn_without_ui": qwen_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 6144,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "qwen-plus": {
                "fn_with_ui": qwen_ui,
                "fn_without_ui": qwen_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 30720,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "qwen-max": {
                "fn_with_ui": qwen_ui,
                "fn_without_ui": qwen_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 28672,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
# -=-=-=-=-=-=- Zero-One Universe Model
yi_models = ["yi-34b-chat-0205","yi-34b-chat-200k","yi-large","yi-medium","yi-spark","yi-large-turbo","yi-large-preview"]
if any(item in yi_models for item in AVAIL_LLM_MODELS):
    try:
        yimodel_4k_noui, yimodel_4k_ui = get_predict_function(
            api_key_conf_name="YIMODEL_API_KEY", max_output_token=600, disable_proxy=False
            )
        yimodel_16k_noui, yimodel_16k_ui = get_predict_function(
            api_key_conf_name="YIMODEL_API_KEY", max_output_token=4000, disable_proxy=False
            )
        yimodel_200k_noui, yimodel_200k_ui = get_predict_function(
            api_key_conf_name="YIMODEL_API_KEY", max_output_token=4096, disable_proxy=False
            )
        model_info.update({
            "yi-34b-chat-0205": {
                "fn_with_ui": yimodel_4k_ui,
                "fn_without_ui": yimodel_4k_noui,
                "can_multi_thread": False,  # Currently，Default to a very low level of concurrency，Therefore disabled
                "endpoint": yimodel_endpoint,
                "max_token": 4000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "yi-34b-chat-200k": {
                "fn_with_ui": yimodel_200k_ui,
                "fn_without_ui": yimodel_200k_noui,
                "can_multi_thread": False,  # Currently，Default to a very low level of concurrency，Therefore disabled
                "endpoint": yimodel_endpoint,
                "max_token": 200000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "yi-large": {
                "fn_with_ui": yimodel_16k_ui,
                "fn_without_ui": yimodel_16k_noui,
                "can_multi_thread": False,  # Currently，Default to a very low level of concurrency，Therefore disabled
                "endpoint": yimodel_endpoint,
                "max_token": 16000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "yi-medium": {
                "fn_with_ui": yimodel_16k_ui,
                "fn_without_ui": yimodel_16k_noui,
                "can_multi_thread": True,  # This concurrency is slightly larger
                "endpoint": yimodel_endpoint,
                "max_token": 16000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "yi-spark": {
                "fn_with_ui": yimodel_16k_ui,
                "fn_without_ui": yimodel_16k_noui,
                "can_multi_thread": True,  # This concurrency is slightly larger
                "endpoint": yimodel_endpoint,
                "max_token": 16000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "yi-large-turbo": {
                "fn_with_ui": yimodel_16k_ui,
                "fn_without_ui": yimodel_16k_noui,
                "can_multi_thread": False,  # Currently，Default to a very low level of concurrency，Therefore disabled
                "endpoint": yimodel_endpoint,
                "max_token": 16000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "yi-large-preview": {
                "fn_with_ui": yimodel_16k_ui,
                "fn_without_ui": yimodel_16k_noui,
                "can_multi_thread": False,  # Currently，Default to a very low level of concurrency，Therefore disabled
                "endpoint": yimodel_endpoint,
                "max_token": 16000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
        })
    except:
        print(trimmed_format_exc())
# -=-=-=-=-=-=- iFLYTEK Spark Cognitive Model -=-=-=-=-=-=-=-=-=-
if "spark" in AVAIL_LLM_MODELS:
    try:
        from void_terminal.request_llms.bridge_spark import predict_no_ui_long_connection as spark_noui
        from void_terminal.request_llms.bridge_spark import predict as spark_ui
        model_info.update({
            "spark": {
                "fn_with_ui": spark_ui,
                "fn_without_ui": spark_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
if "sparkv2" in AVAIL_LLM_MODELS:   # Xunfei Xinghuo cognitive model
    try:
        from void_terminal.request_llms.bridge_spark import predict_no_ui_long_connection as spark_noui
        from void_terminal.request_llms.bridge_spark import predict as spark_ui
        model_info.update({
            "sparkv2": {
                "fn_with_ui": spark_ui,
                "fn_without_ui": spark_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
if "sparkv3" in AVAIL_LLM_MODELS or "sparkv3.5" in AVAIL_LLM_MODELS:   # Xunfei Xinghuo cognitive model
    try:
        from void_terminal.request_llms.bridge_spark import predict_no_ui_long_connection as spark_noui
        from void_terminal.request_llms.bridge_spark import predict as spark_ui
        model_info.update({
            "sparkv3": {
                "fn_with_ui": spark_ui,
                "fn_without_ui": spark_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "sparkv3.5": {
                "fn_with_ui": spark_ui,
                "fn_without_ui": spark_noui,
                "can_multi_thread": True,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
if "llama2" in AVAIL_LLM_MODELS:   # llama2
    try:
        from void_terminal.request_llms.bridge_llama2 import predict_no_ui_long_connection as llama2_noui
        from void_terminal.request_llms.bridge_llama2 import predict as llama2_ui
        model_info.update({
            "llama2": {
                "fn_with_ui": llama2_ui,
                "fn_without_ui": llama2_noui,
                "endpoint": None,
                "max_token": 4096,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
# -=-=-=-=-=-=- ZhiPu -=-=-=-=-=-=-
if "zhipuai" in AVAIL_LLM_MODELS:   # zhipuai is an alias for glm-4，Backward compatible configuration
    try:
        model_info.update({
            "zhipuai": {
                "fn_with_ui": zhipu_ui,
                "fn_without_ui": zhipu_noui,
                "endpoint": None,
                "max_token": 10124 * 8,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
        })
    except:
        print(trimmed_format_exc())
# -=-=-=-=-=-=- Deep Seek Large Model -=-=-=-=-=-=-
if "deepseekcoder" in AVAIL_LLM_MODELS:   # deepseekcoder
    try:
        from void_terminal.request_llms.bridge_deepseekcoder import predict_no_ui_long_connection as deepseekcoder_noui
        from void_terminal.request_llms.bridge_deepseekcoder import predict as deepseekcoder_ui
        model_info.update({
            "deepseekcoder": {
                "fn_with_ui": deepseekcoder_ui,
                "fn_without_ui": deepseekcoder_noui,
                "endpoint": None,
                "max_token": 2048,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            }
        })
    except:
        print(trimmed_format_exc())
# -=-=-=-=-=-=- Magic Square - Deep Quest Large Model Online API -=-=-=-=-=-=-
if "deepseek-chat" in AVAIL_LLM_MODELS or "deepseek-coder" in AVAIL_LLM_MODELS:
    try:
        deepseekapi_noui, deepseekapi_ui = get_predict_function(
            api_key_conf_name="DEEPSEEK_API_KEY", max_output_token=4096, disable_proxy=False
            )
        model_info.update({
            "deepseek-chat":{
                "fn_with_ui": deepseekapi_ui,
                "fn_without_ui": deepseekapi_noui,
                "endpoint": deepseekapi_endpoint,
                "can_multi_thread": True,
                "max_token": 32000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
            "deepseek-coder":{
                "fn_with_ui": deepseekapi_ui,
                "fn_without_ui": deepseekapi_noui,
                "endpoint": deepseekapi_endpoint,
                "can_multi_thread": True,
                "max_token": 16000,
                "tokenizer": tokenizer_gpt35,
                "token_cnt": get_token_num_gpt35,
            },
        })
    except:
        print(trimmed_format_exc())
# -=-=-=-=-=-=- one-api alignment support -=-=-=-=-=-=-
for model in [m for m in AVAIL_LLM_MODELS if m.startswith("one-api-")]:
    # To access the one-api multi-model management interface more flexibly，Designed this interface，Example：AVAIL_LLM_MODELS = ["one-api-mixtral-8x7b(max_token=6666)"]
    # Among them
    #   "one-api-"          Is a prefix（Necessary）
    #   "mixtral-8x7b"      Is model name（Necessary）
    #   "(max_token=6666)"  是配置（Not necessary）
    try:
        _, max_token_tmp = read_one_api_model_name(model)
    except:
        print(f"one-api model {model} The max_token configuration is not an integer，Please check the configuration file。")
        continue
    model_info.update({
        model: {
            "fn_with_ui": chatgpt_ui,
            "fn_without_ui": chatgpt_noui,
            "can_multi_thread": True,
            "endpoint": openai_endpoint,
            "max_token": max_token_tmp,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
# -=-=-=-=-=-=- VLLM alignment support -=-=-=-=-=-=-
for model in [m for m in AVAIL_LLM_MODELS if m.startswith("vllm-")]:
    # To more flexibly access the vllm multi-model management interface，Designed this interface，Example：AVAIL_LLM_MODELS = ["vllm-/home/hmp/llm/cache/Qwen1___5-32B-Chat(max_token=6666)"]
    # Among them
    #   "vllm-"             Is a prefix（Necessary）
    #   "mixtral-8x7b"      Is model name（Necessary）
    #   "(max_token=6666)"  是配置（Not necessary）
    try:
        _, max_token_tmp = read_one_api_model_name(model)
    except:
        print(f"VLLM model {model} The max_token configuration is not an integer，Please check the configuration file。")
        continue
    model_info.update({
        model: {
            "fn_with_ui": chatgpt_ui,
            "fn_without_ui": chatgpt_noui,
            "can_multi_thread": True,
            "endpoint": openai_endpoint,
            "max_token": max_token_tmp,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })
# -=-=-=-=-=-=- ollama alignment support -=-=-=-=-=-=-
for model in [m for m in AVAIL_LLM_MODELS if m.startswith("ollama-")]:
    from void_terminal.request_llms.bridge_ollama import predict_no_ui_long_connection as ollama_noui
    from void_terminal.request_llms.bridge_ollama import predict as ollama_ui
    break
for model in [m for m in AVAIL_LLM_MODELS if m.startswith("ollama-")]:
    # In order to more flexibly access the ollama multi-model management interface，Designed this interface，Example：AVAIL_LLM_MODELS = ["ollama-phi3(max_token=6666)"]
    # Among them
    #   "ollama-"           Is a prefix（Necessary）
    #   "phi3"            Is model name（Necessary）
    #   "(max_token=6666)"  是配置（Not necessary）
    try:
        _, max_token_tmp = read_one_api_model_name(model)
    except:
        print(f"Ollama model {model} The max_token configuration is not an integer，Please check the configuration file。")
        continue
    model_info.update({
        model: {
            "fn_with_ui": ollama_ui,
            "fn_without_ui": ollama_noui,
            "endpoint": ollama_endpoint,
            "max_token": max_token_tmp,
            "tokenizer": tokenizer_gpt35,
            "token_cnt": get_token_num_gpt35,
        },
    })

# -=-=-=-=-=-=- Azure model alignment support -=-=-=-=-=-=-
AZURE_CFG_ARRAY = get_conf("AZURE_CFG_ARRAY") # <-- Used to define and switch between multiple Azure models -->
if len(AZURE_CFG_ARRAY) > 0:
    for azure_model_name, azure_cfg_dict in AZURE_CFG_ARRAY.items():
        # May overwrite previous configuration，But this is expected
        if not azure_model_name.startswith('azure'):
            raise ValueError("The models configured in AZURE_CFG_ARRAY must start with `azure`")
        endpoint_ = azure_cfg_dict["AZURE_ENDPOINT"] + \
            f'openai/deployments/{azure_cfg_dict["AZURE_ENGINE"]}/chat/completions?api-version=2023-05-15'
        model_info.update({
            azure_model_name: {
                "fn_with_ui": chatgpt_ui,
                "fn_without_ui": chatgpt_noui,
                "endpoint": endpoint_,
                "azure_api_key": azure_cfg_dict["AZURE_API_KEY"],
                "max_token": azure_cfg_dict["AZURE_MODEL_MAX_TOKEN"],
                "tokenizer": tokenizer_gpt35,   # The tokenizer is only used to estimate the number of tokens
                "token_cnt": get_token_num_gpt35,
            }
        })
        if azure_model_name not in AVAIL_LLM_MODELS:
            AVAIL_LLM_MODELS += [azure_model_name]


# -=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=-=-=
# -=-=-=-=-=-=-=-=-=- ☝️ The above is the model route -=-=-=-=-=-=-=-=-=
# -=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=-=-=

# -=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=-=-=
# -=-=-=-=-=-=-= 👇 The following is a multi-model route switching function -=-=-=-=-=-=-=
# -=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=--=-=-=-=-=-=-=-=


def LLM_CATCH_EXCEPTION(f):
    """
    Decorator function，Display errors
    """
    def decorated(inputs:str, llm_kwargs:dict, history:list, sys_prompt:str, observe_window:list, console_slience:bool):
        try:
            return f(inputs, llm_kwargs, history, sys_prompt, observe_window, console_slience)
        except Exception as e:
            tb_str = '\n```\n' + trimmed_format_exc() + '\n```\n'
            observe_window[0] = tb_str
            return tb_str
    return decorated


def predict_no_ui_long_connection(inputs:str, llm_kwargs:dict, history:list, sys_prompt:str, observe_window:list=[], console_slience:bool=False):
    """
    Send to LLM，Waiting for reply，Completed in one go，Do not display intermediate processes。But internally（As much as possible）Use the stream method to avoid the cable being disconnected midway。
    inputs：
        This is the input of this inquiry
    sys_prompt:
        System silent prompt
    llm_kwargs：
        LLM`s internal tuning parameters
    history：
        history is the list of previous conversations
    observe_window = None：
        Used to transfer the already output part across threads，Most of the time it`s just for fancy visual effects，Leave it blank。observe_window[0]：Observation window。observe_window[1]：Watchdog
    """
    import threading, time, copy

    inputs = apply_gpt_academic_string_mask(inputs, mode="show_llm")
    model = llm_kwargs['llm_model']
    n_model = 1
    if '&' not in model:
        # If only asking about `one` large language model（In most cases）：
        method = model_info[model]["fn_without_ui"]
        return method(inputs, llm_kwargs, history, sys_prompt, observe_window, console_slience)
    else:
        # If inquiring about `multiple` large language models at the same time，This is a bit verbose，But the idea is the same，You don`t have to read this else branch
        executor = ThreadPoolExecutor(max_workers=4)
        models = model.split('&')
        n_model = len(models)

        window_len = len(observe_window)
        assert window_len==3
        window_mutex = [["", time.time(), ""] for _ in range(n_model)] + [True]

        futures = []
        for i in range(n_model):
            model = models[i]
            method = model_info[model]["fn_without_ui"]
            llm_kwargs_feedin = copy.deepcopy(llm_kwargs)
            llm_kwargs_feedin['llm_model'] = model
            future = executor.submit(LLM_CATCH_EXCEPTION(method), inputs, llm_kwargs_feedin, history, sys_prompt, window_mutex[i], console_slience)
            futures.append(future)

        def mutex_manager(window_mutex, observe_window):
            while True:
                time.sleep(0.25)
                if not window_mutex[-1]: break
                # Watchdog（watchdog）
                for i in range(n_model):
                    window_mutex[i][1] = observe_window[1]
                # Observation window（window）
                chat_string = []
                for i in range(n_model):
                    color = colors[i%len(colors)]
                    chat_string.append( f"【{str(models[i])} Say】: <font color=\"{color}\"> {window_mutex[i][0]} </font>" )
                res = '<br/><br/>\n\n---\n\n'.join(chat_string)
                # # # # # # # # # # #
                observe_window[0] = res

        t_model = threading.Thread(target=mutex_manager, args=(window_mutex, observe_window), daemon=True)
        t_model.start()

        return_string_collect = []
        while True:
            worker_done = [h.done() for h in futures]
            if all(worker_done):
                executor.shutdown()
                break
            time.sleep(1)

        for i, future in enumerate(futures):  # wait and get
            color = colors[i%len(colors)]
            return_string_collect.append( f"【{str(models[i])} Say】: <font color=\"{color}\"> {future.result()} </font>" )

        window_mutex[-1] = False # stop mutex thread
        res = '<br/><br/>\n\n---\n\n'.join(return_string_collect)
        return res

# Adjust the model type according to the ModelOverride parameter in the basic function area，Used for `predict` In
import importlib
import core_functional
def execute_model_override(llm_kwargs, additional_fn, method):
    functional = core_functional.get_core_functions()
    if (additional_fn in functional) and 'ModelOverride' in functional[additional_fn]:
        # Hot update Prompt & ModelOverride
        importlib.reload(core_functional)
        functional = core_functional.get_core_functions()
        model_override = functional[additional_fn]['ModelOverride']
        if model_override not in model_info:
            raise ValueError(f"模型覆盖Parameters '{model_override}' 指To一items暂不支持的模型，Please check the configuration file。")
        method = model_info[model_override]["fn_with_ui"]
        llm_kwargs['llm_model'] = model_override
        return llm_kwargs, additional_fn, method
    # Return the original parameters by default
    return llm_kwargs, additional_fn, method

def predict(inputs:str, llm_kwargs:dict, plugin_kwargs:dict, chatbot,
            history:list=[], system_prompt:str='', stream:bool=True, additional_fn:str=None):
    """
    Send to LLM，Get output in a streaming way。
    Used for basic conversation functions。

    Complete parameter list：
        predict(
            inputs:str,                     # This is the input of this inquiry
            llm_kwargs:dict,                # Is an internal tuning parameter of LLM
            plugin_kwargs:dict,             # Is an internal parameter of the plugin
            chatbot:ChatBotWithCookies,     # Pass through as is，Responsible for displaying dialogue to the user frontend，Take into account the functionality of the frontend state
            history:list=[],                # history is the list of previous conversations
            system_prompt:str='',           # System silent prompt
            stream:bool=True,               # Whether to stream output（Deprecated）
            additional_fn:str=None          # Additional functions of the basic functional area buttons
        ):
    """

    inputs = apply_gpt_academic_string_mask(inputs, mode="show_llm")

    method = model_info[llm_kwargs['llm_model']]["fn_with_ui"]  # If there is an error here，Check the AVAIL_LLM_MODELS option in config

    if additional_fn: # Adjust the model type according to the ModelOverride parameter in the basic function area
        llm_kwargs, additional_fn, method = execute_model_override(llm_kwargs, additional_fn, method)

    yield from method(inputs, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, stream, additional_fn)

