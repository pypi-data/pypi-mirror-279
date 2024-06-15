"""
    All the following configurations can also be overridden using environment variables，See docker-compose.yml for the format of environment variable configuration。
    Read priority：Environment variable > config_private.py > config.py
    --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
    All the following configurations also support using environment variables to override,
    and the environment variable configuration format can be seen in docker-compose.yml.
    Configuration reading priority: environment variable > config_private.py > config.py
"""

# [step 1]>> API_KEY = "sk-123456789xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx123456789"。In very few cases，You also need to fill in the organization（In the format of org-123456789abcdefghijklmno），Please scroll down，Find API_ORG setting item
API_KEY = "Fill in the API key here"    # Multiple API-KEYs can be filled in at the same time，Separated by commas，For exampleAPI_KEY = "sk-openaikey1,sk-openaikey2,fkxxxx-api2dkey3,azure-apikey4"


# [step 2]>> Change to True to apply proxy，If deployed directly on overseas servers，Do not modify here; if using local or region-unrestricted large models，No modification is needed here
USE_PROXY = False
if USE_PROXY:
    """
    Address of the proxy network，Open your proxy software to view the proxy agreement(socks5h / http)and address(localhost)and port(11284)
    Format for filling in is [Protocol]://  [Address] :[Port]，Don`t forget to change USE_PROXY to True before filling in，If deployed directly on overseas servers，Do not modify here
            <Configuration tutorial & video tutorial> https://github.com/binary-husky/gpt_academic/issues/1>
    [Protocol] Common protocols are nothing but socks5h/http; For example, the default local protocol for v2**y and ss* is socks5h; While the default local protocol for cl**h is http
    [Address] Fill in localhost or 127.0.0.1（localhost means that the proxy software is installed on the local machine）
    [Port] Look for it in the settings of the proxy software。Although the interface of different proxy software is different，But the port number should be in the most prominent position
    """
    proxies = {
        #          [Protocol]://  [Address]  :[Port]
        "http":  "socks5h://localhost:11284",  # 再For example  "http":  "http://127.0.0.1:7890",
        "https": "socks5h://localhost:11284",  # 再For example  "https": "http://127.0.0.1:7890",
    }
else:
    proxies = None

# [step 3]>> Model selection is (Attention: LLM_MODEL is the default selected model, It *must* be included in the AVAIL_LLM_MODELS list )
LLM_MODEL = "gpt-3.5-turbo-16k" # Optional ↓↓↓
AVAIL_LLM_MODELS = ["gpt-4-1106-preview", "gpt-4-turbo-preview", "gpt-4-vision-preview",
                    "gpt-4o", "gpt-4-turbo", "gpt-4-turbo-2024-04-09",
                    "gpt-3.5-turbo-1106", "gpt-3.5-turbo-16k", "gpt-3.5-turbo", "azure-gpt-3.5",
                    "gpt-4", "gpt-4-32k", "azure-gpt-4", "glm-4", "glm-4v", "glm-3-turbo",
                    "gemini-pro", "chatglm3"
                    ]
# --- --- --- ---
# P.S. Other available models include
# AVAIL_LLM_MODELS = [
#   "glm-4-0520", "glm-4-air", "glm-4-airx", "glm-4-flash",
#   "qianfan", "deepseekcoder",
#   "spark", "sparkv2", "sparkv3", "sparkv3.5",
#   "qwen-turbo", "qwen-plus", "qwen-max", "qwen-local",
#   "moonshot-v1-128k", "moonshot-v1-32k", "moonshot-v1-8k",
#   "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k-0613", "gpt-3.5-turbo-0125", "gpt-4o-2024-05-13"
#   "claude-3-haiku-20240307","claude-3-sonnet-20240229","claude-3-opus-20240229", "claude-2.1", "claude-instant-1.2",
#   "moss", "llama2", "chatglm_onnx", "internlm", "jittorllms_pangualpha", "jittorllms_llama",
#   "deepseek-chat" ,"deepseek-coder",
#   "yi-34b-chat-0205","yi-34b-chat-200k","yi-large","yi-medium","yi-spark","yi-large-turbo","yi-large-preview",
# ]
# --- --- --- ---
# In addition，You can also access one-api/vllm/ollama，
# Use"one-api-*","vllm-*","ollama-*"Prefix直接Use非标准方式接入的模型，For example
# AVAIL_LLM_MODELS = ["one-api-claude-3-sonnet-20240229(max_token=100000)", "ollama-phi3(max_token=4096)"]
# --- --- --- ---


# --------------- The following configurations can optimize the experience ---------------

# Redirect URL，Realize the function of changing API_URL（High-risk setting! Do not modify under normal circumstances! Modify this setting，You will completely expose your API-KEY and conversation privacy to the middleman you set!）
# Format: API_URL_REDIRECT = {"https://api.openai.com/v1/chat/completions": "In这里填写重定To的api.openai.com的URL"}
# For example: API_URL_REDIRECT = {"https://api.openai.com/v1/chat/completions": "https://reverse-proxy-url/v1/chat/completions", "http://localhost:11434/api/chat": "In这里填写您ollama的URL"}
API_URL_REDIRECT = {}


# In the multi-threaded function plugin，How many threads are allowed to access OpenAI at the same time by default。The limit for free trial users is 3 times per minute，The limit for Pay-as-you-go users is 3500 times per minute
# In short：Free（5 dollars）User fills in 3，Users who have bound their credit card to OpenAI can fill in 16 or higher。Please check for higher limits：https://platform.openai.com/docs/guides/rate-limits/overview
DEFAULT_WORKER_NUM = 3


# Color theme, Optional ["Default", "Chuanhu-Small-and-Beautiful", "High-Contrast"]
# More themes, Please refer to the Gradio theme store: https://huggingface.co/spaces/gradio/theme-gallery optional ["Gstaff/Xkcd", "NoCrypt/Miku", ...]
THEME = "Default"
AVAIL_THEMES = ["Default", "Chuanhu-Small-and-Beautiful", "High-Contrast", "Gstaff/Xkcd", "NoCrypt/Miku"]


# Default system prompts（system prompt）
INIT_SYS_PROMPT = "Serve me as a writing and programming assistant."


# Height of the Conversation Window （仅InLAYOUT="TOP-DOWN"When生效）
CHATBOT_HEIGHT = 1115


# Code Highlighting
CODE_HIGHLIGHT = True


# Window Layout
LAYOUT = "LEFT-RIGHT"   # "LEFT-RIGHT"（Horizontal Layout） # "TOP-DOWN"（Vertical Layout）


# Dark mode / Light mode
DARK_MODE = True


# After sending the request to OpenAI，Timeout Threshold
TIMEOUT_SECONDS = 30


# Web Port, -1 represents random port
WEB_PORT = -1


# Whether to automatically open the browser page
AUTO_OPEN_BROWSER = True


# If OpenAI does not respond（Network Lag, Proxy Failure, KEY Invalid），Retry Limit
MAX_RETRY = 2


# Default options for plugin classification
DEFAULT_FN_GROUPS = ['Conversation', 'programming', 'Academic', 'Intelligent agent']


# Define which models the `Ask multiple GPT models` plugin should use on the interface，Please select from AVAIL_LLM_MODELS，And use it between different models`&`Interval，For example"gpt-3.5-turbo&chatglm3&azure-gpt-4"
MULTI_QUERY_LLM_MODELS = "gpt-3.5-turbo&chatglm3"


# Choose the local model variant（Only when AVAIL_LLM_MODELS contains the corresponding local model，Will take effect）
# TranslatedText，So please specify the specific model in QWEN_MODEL_SELECTION below
# It can also be a specific model path
QWEN_LOCAL_MODEL_SELECTION = "Qwen/Qwen-1_8B-Chat-Int8"


# Access TongYi QianWen Online Large Model HTTPS://dashscope.console.aliyun.com/
DASHSCOPE_API_KEY = "" # Aliyun API_KEY


# Baidu Qianfan（LLM_MODEL="qianfan"）
BAIDU_CLOUD_API_KEY = ''
BAIDU_CLOUD_SECRET_KEY = ''
BAIDU_CLOUD_QIANFAN_MODEL = 'ERNIE-Bot'    # Optional "ERNIE-Bot-4"(Wenxin Large Model 4.0), "ERNIE-Bot"(Original text), "ERNIE-Bot-turbo", "BLOOMZ-7B", "Llama-2-70B-Chat", "Llama-2-13B-Chat", "Llama-2-7B-Chat", "ERNIE-Speed-128K", "ERNIE-Speed-8K", "ERNIE-Lite-8K"


# If using ChatGLM2 fine-tuning model，请把 LLM_MODEL="chatglmft"，And specify the model path here
CHATGLM_PTUNING_CHECKPOINT = "" # For example"/home/hmp/ChatGLM2-6B/ptuning/output/6b-pt-128-1e-2/checkpoint-100"


# Execution mode of local LLM models such as ChatGLM CPU/GPU
LOCAL_MODEL_DEVICE = "cpu" # Optional "cuda"
LOCAL_MODEL_QUANT = "FP16" # Default "FP16" "INT4" 启用量化INT4version本 "INT8" 启用量化INT8version本


# Set the number of parallel threads for Gradio（No modification is needed）
CONCURRENT_COUNT = 100


# Whether to automatically clear the input box upon submission
AUTO_CLEAR_TXT = False


# Add a Live2D decoration
ADD_WAIFU = False


# Set username and password（No modification is needed）（Related functions are unstable，Related to gradio version and network，Not recommended to add this for local use）
# [("username", "password"), ("username2", "password2"), ...]
AUTHENTICATION = []


# If you need to run under the second-level path（Under normal circumstances，Do not modify!!）
# （For example CUSTOM_PATH = "/gpt_academic"，Can Run the Software Over HTTP://ip:Under port/gpt_academic/。）
CUSTOM_PATH = "/"


# HTTPS Key and Certificate（No modification is needed）
SSL_KEYFILE = ""
SSL_CERTFILE = ""


# In very few cases，Openai`s official KEY needs to be accompanied by organizational code（Format like org-xxxxxxxxxxxxxxxxxxxxxxxx）Use
API_ORG = ""


# If you need to use Slack Claude，See request_llms/README.md for detailed usage instructions
SLACK_CLAUDE_BOT_ID = ''
SLACK_CLAUDE_USER_TOKEN = ''


# If you need to use AZURE（Method 1：Deploy a single Azure model）For details, please refer to the additional document docs\use_azure.md
AZURE_ENDPOINT = "https://The API name you wrote yourself.openai.azure.com/"
AZURE_API_KEY = "Fill in the Azure OpenAI API key"    # It is recommended to fill in directly at API_KEY.，This option will be deprecated soon
AZURE_ENGINE = "Fill in the deployment name you wrote by yourself"            # Read docs\use_azure.md


# If you need to use AZURE（Method 2：Deploy multiple Azure models + dynamic switching）For details, please refer to the additional document docs\use_azure.md
AZURE_CFG_ARRAY = {}


# Alibaba Cloud real-time speech recognition has a higher configuration difficulty
# Refer to https://github.com/binary-husky/gpt_academic/blob/master/docs/use_audio.md
ENABLE_AUDIO = False
ALIYUN_TOKEN=""     # For example, f37f30e0f9934c34a992f6f64f7eba4f
ALIYUN_APPKEY=""    # For example, RoPlZrM88DnAFkZK
ALIYUN_ACCESSKEY="" # （No need to fill in）
ALIYUN_SECRET=""    # （No need to fill in）


# Operating address of GPT-SOVITS text-to-speech service（Read aloud the generated text of the language model）
TTS_TYPE = "EDGE_TTS" # EDGE_TTS / LOCAL_SOVITS_API / DISABLE
GPT_SOVITS_URL = ""
EDGE_TTS_VOICE = "zh-CN-XiaoxiaoNeural"


# Access to Xunfei Xinghuo large model https://console.xfyun.cn/services/iat
XFYUN_APPID = "00000000"
XFYUN_API_SECRET = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
XFYUN_API_KEY = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


# Access the intelligent spectrum model
ZHIPUAI_API_KEY = ""
ZHIPUAI_MODEL = "" # This option is deprecated，No longer needs to be filled out


# Claude API KEY
ANTHROPIC_API_KEY = ""


# Dark side of the moon API KEY
MOONSHOT_API_KEY = ""


# Zero One Universe(Yi Model) API KEY
YIMODEL_API_KEY = ""

# Deep Search(DeepSeek) API KEY，Default请求Address为"https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = ""

# Mathpix has OCR functionality for PDFs，But registration is required
MATHPIX_APPID = ""
MATHPIX_APPKEY = ""


# PDF parsing service of DOC2X，Register an account and get an API KEY: https://doc2x.noedgeai.com/login
DOC2X_API_KEY = ""


# Customize API KEY format
CUSTOM_API_KEY_PATTERN = ""


# Google Gemini API-Key
GEMINI_API_KEY = ''


# HUGGINGFACE`s TOKEN，Works when downloading LLAMA https://huggingface.co/docs/hub/security-tokens
HUGGINGFACE_ACCESS_TOKEN = "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"


# GROBID server address（Filling in multiple can balance the load），Used for high-quality reading of PDF documents
# Get method：Copy the following space https://huggingface.co/spaces/qingxu98/grobid，Set as public，然后GROBID_URL = "https://(Your hf username is qingxu98)-(Your filled space name such as grobid).hf.space"
GROBID_URLS = [
    "https://qingxu98-grobid.hf.space","https://qingxu98-grobid2.hf.space","https://qingxu98-grobid3.hf.space",
    "https://qingxu98-grobid4.hf.space","https://qingxu98-grobid5.hf.space", "https://qingxu98-grobid6.hf.space",
    "https://qingxu98-grobid7.hf.space", "https://qingxu98-grobid8.hf.space",
]


# Allow modifying the configuration of this page through natural language description，This feature has a certain level of danger，Default closed
ALLOW_RESET_CONFIG = False


# When using the AutoGen plugin，Whether to run the code using Docker container
AUTOGEN_USE_DOCKER = False


# Temporary upload folder location，Please do not modify
PATH_PRIVATE_UPLOAD = "private_upload"


# Location of the log folder，Please do not modify
PATH_LOGGING = "gpt_log"


# In addition to connecting OpenAI，What other occasions allow the use of proxies，Please do not modify
WHEN_TO_USE_PROXY = ["Download_LLM", "Download_Gradio_Theme", "Connect_Grobid",
                     "Warmup_Modules", "Nougat_Download", "AutoGen"]


# *Experimental feature*: Automatically detect and block invalid keys，Please do not use
BLOCK_INVALID_APIKEY = False


# Enable plugin hot reload
PLUGIN_HOT_RELOAD = False


# Maximum number limit for custom buttons
NUM_CUSTOM_BASIC_BTN = 4



"""
--------------- Configuration relationship description ---------------

Online large model configuration relationship diagram
│
├── "gpt-3.5-turbo" etc.openai模型
│   ├── API_KEY
│   ├── CUSTOM_API_KEY_PATTERN（Not commonly used）
│   ├── API_ORG（Not commonly used）
│   └── API_URL_REDIRECT（Not commonly used）
│
├── "azure-gpt-3.5" etc.azure模型（Single Azure model，No need for dynamic switching）
│   ├── API_KEY
│   ├── AZURE_ENDPOINT
│   ├── AZURE_API_KEY
│   ├── AZURE_ENGINE
│   └── API_URL_REDIRECT
│
├── "azure-gpt-3.5" etc.azure模型（Multiple Azure models，Dynamic switching is required，High priority）
│   └── AZURE_CFG_ARRAY
│
├── "spark" Spark Cognitive Big Model spark & sparkv2
│   ├── XFYUN_APPID
│   ├── XFYUN_API_SECRET
│   └── XFYUN_API_KEY
│
├── "claude-3-opus-20240229" etc.claude模型
│   └── ANTHROPIC_API_KEY
│
├── "stack-claude"
│   ├── SLACK_CLAUDE_BOT_ID
│   └── SLACK_CLAUDE_USER_TOKEN
│
├── "qianfan" Baidu QianfanLarge Model库
│   ├── BAIDU_CLOUD_QIANFAN_MODEL
│   ├── BAIDU_CLOUD_API_KEY
│   └── BAIDU_CLOUD_SECRET_KEY
│
├── "glm-4", "glm-3-turbo", "zhipuai" Zhipu AI large model
│   └── ZHIPUAI_API_KEY
│
├── "yi-34b-chat-0205", "yi-34b-chat-200k" etc.Zero One Universe(Yi Model)Large Model
│   └── YIMODEL_API_KEY
│
├── "qwen-turbo" etc.通义千AskLarge Model
│   └──  DASHSCOPE_API_KEY
│
├── "Gemini"
│   └──  GEMINI_API_KEY
│
└── "one-api-...(max_token=...)" 用一种更方便的方式接入one-api多模型管理界面
    ├── AVAIL_LLM_MODELS
    ├── API_KEY
    └── API_URL_REDIRECT


Local large model diagram
│
├── "chatglm3"
├── "chatglm"
├── "chatglm_onnx"
├── "chatglmft"
├── "internlm"
├── "moss"
├── "jittorllms_pangualpha"
├── "jittorllms_llama"
├── "deepseekcoder"
├── "qwen-local"
Support for RWKV is available in the Wiki
└── "llama2"


Diagram of user interface layout dependencies
│
├── CHATBOT_HEIGHT Height of the chat window
├── CODE_HIGHLIGHT Code highlighting
├── LAYOUT window layout
├── DARK_MODE Dark mode / Light mode
├── DEFAULT_FN_GROUPS Plugin classification default options
├── THEME color theme
├── AUTO_CLEAR_TXT Whether to automatically clear the input box when submitting
├── ADD_WAIFU Add a live2d decoration
└── ALLOW_RESET_CONFIG Whether to allow modifying the configuration of this page through natural language description，This feature has a certain level of danger


Plugin online service configuration dependency diagram
│
├── Voice function
│   ├── ENABLE_AUDIO
│   ├── ALIYUN_TOKEN
│   ├── ALIYUN_APPKEY
│   ├── ALIYUN_ACCESSKEY
│   └── ALIYUN_SECRET
│
└── Accurate parsing of PDF documents
    ├── GROBID_URLS
    ├── MATHPIX_APPID
    └── MATHPIX_APPKEY


"""
