from void_terminal.toolbox import CatchException, update_ui, report_exception
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from void_terminal.crazy_functions.plugin_template.plugin_class_template import (
    GptAcademicPluginTemplate,
)
from void_terminal.crazy_functions.plugin_template.plugin_class_template import ArgProperty

# Here are the PROMPTS for each type of chart
SELECT_PROMPT = """
“{subject}”
=============
The above is an abstract extracted from the article,Will use these summaries to draw charts。Please choose an appropriate chart type:
Flowchart
Sequence diagram 2
3-Class diagram
Pie Chart
5 Gantt chart
State Diagram
7 Entity relationship diagram
8-quadrant prompt diagram
No need to explain the reason，Single digit without any punctuation。
"""
# No mind map!!! Testing found that the model always prioritizes mind maps
# Flowchart
PROMPT_1 = """
Please Provide a Logic Diagram Surrounding `{subject}`，Use mermaid syntax，Note that you need to enclose the content in double quotes。
Mermaid syntax example：
```mermaid
graph TD
    P("programming") --> L1("Python")
    P("programming") --> L2("C")
    P("programming") --> L3("C++")
    P("programming") --> L4("Javascipt")
    P("programming") --> L5("PHP")
```
"""
# Sequence diagram
PROMPT_2 = """
Please provide a sequence diagram around `{subject}`，Use mermaid syntax。
Mermaid syntax example：
```mermaid
sequenceDiagram
    Participant A as User
    participant B as System
    A->>B: Login request
    B->>A: Login successful
    A->>B: Get data
    B->>A: Return Data
```
"""
# Class Diagram
PROMPT_3 = """
Please provide a class diagram around `{subject}`，Use mermaid syntax。
Mermaid syntax example：
```mermaid
classDiagram
    Class01 <|-- AveryLongClass : Cool
    Class03 *-- Class04
    Class05 o-- Class06
    Class07 .. Class08
    Class09 --> C2 : Where am i?
    Class09 --* C3
    Class09 --|> Class07
    Class07 : equals()
    Class07 : Object[] elementData
    Class01 : size()
    Class01 : int chimp
    Class01 : int gorilla
    Class08 <--> C2: Cool label
```
"""
# Pie Chart
PROMPT_4 = """
Please provide a pie chart around `{subject}`，Use mermaid syntax，Note that you need to enclose the content in double quotes。
Mermaid syntax example：
```mermaid
pie title Pets adopted by volunteers
    "Dog" : 386
    "Cat" : 85
    "兔子" : 15
```
"""
# Gantt Chart
PROMPT_5 = """
Please provide a Gantt chart around `{subject}`，Use mermaid syntax，Note that you need to enclose the content in double quotes。
Mermaid syntax example：
```mermaid
gantt
    title "项目开发流程"
    dateFormat  YYYY-MM-DD
    section "设计"
    "Requirement Analysis" :done, des1, 2024-01-06,2024-01-08
    "Prototype design" :active, des2, 2024-01-09, 3d
    "UI design" : des3, after des2, 5d
    section "开发"
    "Front-end development" :2024-01-20, 10d
    "Backend development" :2024-01-20, 10d
```
"""
# State Diagram
PROMPT_6 = """
Please provide a state diagram surrounding `{subject}`，Use mermaid syntax，Note that you need to enclose the content in double quotes。
Mermaid syntax example：
```mermaid
stateDiagram-v2
   [*] --> "Still"
    "Still" --> [*]
    "Still" --> "Moving"
    "Moving" --> "Still"
    "Moving" --> "Crash"
    "Crash" --> [*]
```
"""
# Entity relationship diagram
PROMPT_7 = """
Please provide an entity relationship diagram around `{subject}`，Use mermaid syntax。
Mermaid syntax example：
```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER {
        string name
        string id
    }
    ORDER {
        string orderNumber
        date orderDate
        string customerID
    }
    LINE-ITEM {
        number quantity
        string productID
    }
```
"""
# Quadrant prompt diagram
PROMPT_8 = """
Please provide a quadrant diagram around `{subject}`，Use mermaid syntax，Note that you need to enclose the content in double quotes。
Mermaid syntax example：
```mermaid
graph LR
    A["Hard skill"] --> B("Programming")
    A["Hard skill"] --> C("Design")
    D["Soft skill"] --> E("Coordination")
    D["Soft skill"] --> F("Communication")
```
"""
# Mind map
PROMPT_9 = """
{subject}
==========
Please provide a mind map of the content above，Fully consider the logic between them，Use mermaid syntax，Note that you need to enclose the content in double quotes。
Mermaid syntax example：
```mermaid
mindmap
  root((mindmap))
    ("Origins")
      ("Long history")
      ::icon(fa fa-book)
      ("Popularisation")
        ("British popular psychology author Tony Buzan")
        ::icon(fa fa-user)
    ("Research")
      ("On effectiveness<br/>and features")
      ::icon(fa fa-search)
      ("On Automatic creation")
      ::icon(fa fa-robot)
        ("Uses")
            ("Creative techniques")
            ::icon(fa fa-lightbulb-o)
            ("Strategic planning")
            ::icon(fa fa-flag)
            ("Argument mapping")
            ::icon(fa fa-comments)
    ("Tools")
      ("Pen and paper")
      ::icon(fa fa-pencil)
      ("Mermaid")
      ::icon(fa fa-code)
```
"""


def ParseHistoricalInput(history, llm_kwargs, file_manifest, chatbot, plugin_kwargs):
    ############################## <Step 0，Cut Input> ##################################
    # Use functions from PDF cutting to segment the text
    TOKEN_LIMIT_PER_FRAGMENT = 2500
    txt = (
        str(history).encode("utf-8", "ignore").decode()
    )  # avoid reading non-utf8 chars
    from void_terminal.crazy_functions.pdf_fns.breakdown_txt import (
        breakdown_text_to_satisfy_token_limit,
    )

    txt = breakdown_text_to_satisfy_token_limit(
        txt=txt, limit=TOKEN_LIMIT_PER_FRAGMENT, llm_model=llm_kwargs["llm_model"]
    )
    ############################## <Step 1，iterate through the entire article，extract concise information> ##################################
    results = []
    MAX_WORD_TOTAL = 4096
    n_txt = len(txt)
    last_iteration_result = "Extract Summary from the Following Text。"
    if n_txt >= 20:
        print("Article is too long，Cannot achieve expected results")
    for i in range(n_txt):
        NUM_OF_WORD = MAX_WORD_TOTAL // n_txt
        i_say = f"Read this section, recapitulate the content of this section with less than {NUM_OF_WORD} words in Chinese: {txt[i]}"
        i_say_show_user = f"[{i+1}/{n_txt}] Read this section, recapitulate the content of this section with less than {NUM_OF_WORD} words: {txt[i][:200]} ...."
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            i_say,
            i_say_show_user,  # i_say=questions actually asked to chatgpt， i_say_show_user=questions shown to the user
            llm_kwargs,
            chatbot,
            history=[
                "The main content of the previous section is?",
                last_iteration_result,
            ],  # iterate over the previous result
            sys_prompt="Extracts the main content from the text section where it is located for graphing purposes, answer me with Chinese.",  # prompt
        )
        results.append(gpt_say)
        last_iteration_result = gpt_say
    ############################## <Step 2，Select chart type based on the organized summary> ##################################
    gpt_say = str(plugin_kwargs)  # Set the chart type parameter to the plugin parameter
    results_txt = "\n".join(results)  # Merge Summary
    if gpt_say not in [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    ]:  # If the plugin parameters are incorrect, use the dialogue model for judgment
        i_say_show_user = (
            f"Next, determine the appropriate chart type,If there are 3 consecutive failures, a flowchart will be used to draw"
        )
        gpt_say = "[Local Message] Received。"  # user prompt
        chatbot.append([i_say_show_user, gpt_say])
        yield from update_ui(chatbot=chatbot, history=[])  # Update UI
        i_say = SELECT_PROMPT.format(subject=results_txt)
        i_say_show_user = f'Please determine the suitable flowchart type,The corresponding relationship of the numbers is:1-Flowchart,Sequence Diagram,3-Class Diagram,4-Pie chart,5-Gantt chart,6-State Diagram,7-Entity relationship diagram,8-quadrant prompt diagram。Because regardless of what the provided text is,模型大概率认为"Mind map"最合适,Therefore, the mind map can only be invoked through parameters。'
        for i in range(3):
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs=i_say,
                inputs_show_user=i_say_show_user,
                llm_kwargs=llm_kwargs,
                chatbot=chatbot,
                history=[],
                sys_prompt="",
            )
            if gpt_say in [
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
            ]:  # Determine if the return is correct
                break
        if gpt_say not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            gpt_say = "1"
    ############################## <Step 3，Draw a chart based on the selected chart type> ##################################
    if gpt_say == "1":
        i_say = PROMPT_1.format(subject=results_txt)
    elif gpt_say == "2":
        i_say = PROMPT_2.format(subject=results_txt)
    elif gpt_say == "3":
        i_say = PROMPT_3.format(subject=results_txt)
    elif gpt_say == "4":
        i_say = PROMPT_4.format(subject=results_txt)
    elif gpt_say == "5":
        i_say = PROMPT_5.format(subject=results_txt)
    elif gpt_say == "6":
        i_say = PROMPT_6.format(subject=results_txt)
    elif gpt_say == "7":
        i_say = PROMPT_7.replace("{subject}", results_txt)  # Because the entity relationship diagram uses the {} symbol
    elif gpt_say == "8":
        i_say = PROMPT_8.format(subject=results_txt)
    elif gpt_say == "9":
        i_say = PROMPT_9.format(subject=results_txt)
    i_say_show_user = f"Please draw the corresponding chart based on the judgment result。Please use parameters to call if you need to draw a mind map,Large charts may need to be copied to an online editor for rendering。"
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=i_say,
        inputs_show_user=i_say_show_user,
        llm_kwargs=llm_kwargs,
        chatbot=chatbot,
        history=[],
        sys_prompt="",
    )
    history.append(gpt_say)
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page # UI update


@CatchException
def GenerateMultipleMermaidCharts(
    txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port
):
    """
    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters，Such as temperature and top_p，Generally pass it on as is
    plugin_kwargs   Plugin model parameters，Various parameters used to flexibly adjust complex functions
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    web_port        Current software running port number
    """
    import os

    # Basic information：Function, contributor
    chatbot.append(
        [
            "Function plugin feature？",
            "According to the current chat history or specified path file(File Content Takes Priority)Draw various mermaid charts，The dialogue model will first determine the appropriate chart type，Draw a chart subsequently。\
        \nYou can also specify the type of chart to be drawn using plugin parameters,Function plugin contributor: Menghuan1918",
        ]
    )
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page

    if os.path.exists(txt):  # If the input area is empty, parse the history directly
        from void_terminal.crazy_functions.pdf_fns.parse_word import extract_text_from_files

        file_exist, final_result, page_one, file_manifest, excption = (
            extract_text_from_files(txt, chatbot, history)
        )
    else:
        file_exist = False
        excption = ""
        file_manifest = []

    if excption != "":
        if excption == "word":
            report_exception(
                chatbot,
                history,
                a=f"Parsing project: {txt}",
                b=f".doc file found，But the file format is not supported，Please convert it to .docx format first。",
            )

        elif excption == "pdf":
            report_exception(
                chatbot,
                history,
                a=f"Parsing project: {txt}",
                b=f"Failed to import software dependencies。Using this module requires additional dependencies，Installation method```pip install --upgrade pymupdf```。",
            )

        elif excption == "word_pip":
            report_exception(
                chatbot,
                history,
                a=f"Parsing project: {txt}",
                b=f"Failed to import software dependencies。Using this module requires additional dependencies，Installation method```pip install --upgrade python-docx pywin32```。",
            )

        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page

    else:
        if not file_exist:
            history.append(txt)  # If the input area is not a file, add the content of the input area to the history
            i_say_show_user = f"First, you extract an abstract from the history。"
            gpt_say = "[Local Message] Received。"  # user prompt
            chatbot.append([i_say_show_user, gpt_say])
            yield from update_ui(chatbot=chatbot, history=history)  # Update UI
            yield from ParseHistoricalInput(
                history, llm_kwargs, file_manifest, chatbot, plugin_kwargs
            )
        else:
            file_num = len(file_manifest)
            for i in range(file_num):  # Process files in order
                i_say_show_user = f"[{i+1}/{file_num}]Handle file{file_manifest[i]}"
                gpt_say = "[Local Message] Received。"  # user prompt
                chatbot.append([i_say_show_user, gpt_say])
                yield from update_ui(chatbot=chatbot, history=history)  # Update UI
                history = []  # If the input area content is a file, clear the history
                history.append(final_result[i])
                yield from ParseHistoricalInput(
                    history, llm_kwargs, file_manifest, chatbot, plugin_kwargs
                )


class Mermaid_Gen(GptAcademicPluginTemplate):
    def __init__(self):
        pass

    def define_arg_selection_menu(self):
        gui_definition = {
            "Type_of_Mermaid": ArgProperty(
                title="Types of Mermaid charts drawn",
                options=[
                    "Decided by LLM",
                    "Flowchart",
                    "Sequence diagram",
                    "Class Diagram",
                    "Pie Chart",
                    "Gantt Chart",
                    "State Diagram",
                    "Entity relationship diagram",
                    "Quadrant prompt diagram",
                    "Mind map",
                ],
                default_value="Decided by LLM",
                description="选择'Decided by LLM'WhenConvert由Conversation模型判断适合的图表类型(Excluding mind maps)，Directly draw the specified chart type when selecting another type。",
                type="dropdown",
            ).model_dump_json(),
        }
        return gui_definition

    def execute(
        txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request
    ):
        options = [
            "Decided by LLM",
            "Flowchart",
            "Sequence diagram",
            "Class Diagram",
            "Pie Chart",
            "Gantt Chart",
            "State Diagram",
            "Entity relationship diagram",
            "Quadrant prompt diagram",
            "Mind map",
        ]
        plugin_kwargs = options.index(plugin_kwargs['Type_of_Mermaid'])
        yield from GenerateMultipleMermaidCharts(
            txt,
            llm_kwargs,
            plugin_kwargs,
            chatbot,
            history,
            system_prompt,
            user_request,
        )
