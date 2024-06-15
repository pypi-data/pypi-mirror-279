from void_terminal.toolbox import CatchException, update_ui
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
import datetime

####################################################################################################################
# Demo 1: A very simple plugin #########################################################################################
####################################################################################################################

HighOrderFunctionTemplateDiagram = f"""
```mermaid
flowchart TD
    %% <gpt_academic_hide_mermaid_code> A special mark，Used to hide code blocks when generating mermaid charts
    subgraph function call["函数Call过程"]
        AA["Text entered by the user in the input field(txt)"] --> BB["GPT model parameters(llm_kwargs)"]
        BB --> CC["PluginModel parameters(plugin_kwargs)"]
        CC --> DD["Conversation显示框的句柄(chatbot)"]
        DD --> EE["Conversation history(history)"]
        EE --> FF["Systemprompt词(system_prompt)"]
        FF --> GG["当前用户信息(web_port)"]

        A["Start(Query 5-Day Historical Events)"]
        A --> B["获取当前Month份andDay期"]
        B --> C["生成History事件查询prompt词"]
        C --> D["CallLarge Model"]
        D --> E["更新界面"]
        E --> F["记录History"]
        F --> |"下一天"| B
    end
```
"""

@CatchException
def HighOrderFunctionTemplateFunctions(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request, num_day=5):
    """
    # HighOrderFunctionTemplateDiagram：https://mermaid.live/edit#pako:eNptk1tvEkEYhv8KmattQpvlvOyFCcdeeaVXuoYssBwie8gyhCIlqVoLhrbbtAWNUpEGUkyMEDW2Fmn_DDOL_8LZHdOwxrnamX3f7_3mmZk6yKhZCfAgV1KrmYKoQ9fDuKC4yChX0nld1Aou1JzjznQ5fWmejh8LYHW6vG2a47YAnlCLNSIRolnenKBXI_zRIBrcuqRT890u7jZx7zMDt-AaMbnW1--5olGiz2sQjwfoQxsZL0hxplSSU0-rop4vrzmKR6O2JxYjHmwcL2Y_HDatVMkXlf86YzHbGY9bO5j8XE7O8Nsbc3iNB3ukL2SMcH-XIQBgWoVOZzxuOxOJOyc63EPGV6ZQLENVrznViYStTiaJ2vw2M2d9bByRnOXkgCnXylCSU5quyto_IcmkbdvctELmJ-j1ASW3uB3g5xOmKqVTmqr_Na3AtuS_dtBFm8H90XJyHkDDT7S9xXWb4HGmRChx64AOL5HRpUm411rM5uh4H78Z4V7fCZzytjZz2seto9XaNPFue07clLaVZF8UNLygJ-VES8lah_n-O-5Ozc7-77NzJ0-K0yr0ZYrmHdqAk50t2RbA4qq9uNohBASw7YpSgaRkLWCCAtxAlnRZLGbJba9bPwUAC5IsCYAnn1kpJ1ZKUACC0iBSsQLVBzUlA3ioVyQ3qGhZEUrxokiehAz4nFgqk1VNVABfB1uAD_g2_AGPl-W8nMcbCvsDblADfNCz4feyobDPy3rYEMtxwYYbPFNVUoHdCPmDHBv2cP4AMfrCbiBli-Q-3afv0X6WdsIjW2-10fgDy1SAig

    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters，Such as temperature and top_p，Generally pass it on as is
    plugin_kwargs   Plugin model parameters，Various parameters used to flexibly adjust complex functions
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    user_request    Current user`s request information（IP addresses, etc.）
    """
    history = []    # Clear history，To avoid input overflow
    chatbot.append((
        "You are calling a plugin：Today in history",
        "[Local Message] Please note，You are calling a[function plugin]template，This function is aimed at developers who want to implement more interesting features，It can be used as a template for creating new feature functions（This Function Has Only 20+ Lines of Code）。In addition, we also provide a multi-threaded demo that can process a large number of files synchronously for your reference。If you want to share new feature modules，Please don`t hesitate to PR!" + HighOrderFunctionTemplateDiagram))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # As requesting GPT takes some time，Let`s do a UI update in time
    for i in range(int(num_day)):
        currentMonth = (datetime.date.today() + datetime.timedelta(days=i)).month
        currentDay = (datetime.date.today() + datetime.timedelta(days=i)).day
        i_say = f'Which Events Happened in History on{currentMonth}Month{currentDay}Day？List Two and Send Relevant Pictures。When Sending Pictures，Please Use Markdown，Replace PUT_YOUR_QUERY_HERE in the Unsplash API with the Most Important Word Describing the Event。'
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=i_say, inputs_show_user=i_say,
            llm_kwargs=llm_kwargs, chatbot=chatbot, history=[],
            sys_prompt="When you want to send a photo，Please Use Markdown, And do not use backslashes, Do not use code blocks。Use Unsplash API (https://source.unsplash.com/1280x720/? < PUT_YOUR_QUERY_HERE >)。"
        )
        chatbot[-1] = (i_say, gpt_say)
        history.append(i_say);history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update







####################################################################################################################
# Demo 2: A plugin with a secondary menu #######################################################################################
####################################################################################################################

from void_terminal.crazy_functions.plugin_template.plugin_class_template import GptAcademicPluginTemplate, ArgProperty
class Demo_Wrap(GptAcademicPluginTemplate):
    def __init__(self):
        """
        Please note`execute`Will be executed in different threads，So when you define and use class variables，Should be extremely cautious!
        """
        pass

    def define_arg_selection_menu(self):
        """
        Define the secondary option menu of the plugin
        """
        gui_definition = {
            "num_day":
                ArgProperty(title="Date selection", options=["Only today", "Next 3 days", "Next 5 days"], default_value="Next 3 days", description="None", type="dropdown").model_dump_json(),
        }
        return gui_definition

    def execute(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
        """
        Execute the plugin
        """
        num_day = plugin_kwargs["num_day"]
        if num_day == "Only today": num_day = 1
        if num_day == "Next 3 days": num_day = 3
        if num_day == "Next 5 days": num_day = 5
        yield from HighOrderFunctionTemplateFunctions(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request, num_day=num_day)












####################################################################################################################
# Demo 3: Demo for Drawing Mind Maps ############################################################################################
####################################################################################################################

PROMPT = """
Please Provide a Logic Diagram Surrounding `{subject}`，Use mermaid syntax，Mermaid syntax example：
```mermaid
graph TD
    P(programming) --> L1(Python)
    P(programming) --> L2(C)
    P(programming) --> L3(C++)
    P(programming) --> L4(Javascipt)
    P(programming) --> L5(PHP)
```
"""
@CatchException
def test_chart_rendering(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    """
    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters，Such as temperature and top_p，Generally pass it on as is
    plugin_kwargs   Plugin model parameters，Various parameters used to flexibly adjust complex functions
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    user_request    Current user`s request information（IP addresses, etc.）
    """
    history = []    # Clear history，To avoid input overflow
    chatbot.append(("What is this function？", "A function to test the Mermaid chart drawing，You can enter some keywords in the input box，Then use mermaid+llm to draw charts。"))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # As requesting GPT takes some time，Let`s do a UI update in time

    if txt == "": txt = "Blank input field" # Play a joke

    i_say_show_user = f'Please draw something about `{txt}Logic Relationship Diagram。'
    i_say = PROMPT.format(subject=txt)
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=i_say,
        inputs_show_user=i_say_show_user,
        llm_kwargs=llm_kwargs, chatbot=chatbot, history=[],
        sys_prompt=""
    )
    history.append(i_say); history.append(gpt_say)
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # UI update