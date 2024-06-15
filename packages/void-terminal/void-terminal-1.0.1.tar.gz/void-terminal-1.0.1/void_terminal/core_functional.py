# 'primary' 颜色对应 theme.py In的 primary_hue
# 'secondary' 颜色对应 theme.py In的 neutral_hue
# 'stop' 颜色对应 theme.py In的 color_er
import importlib
from void_terminal.toolbox import clear_line_break
from void_terminal.toolbox import apply_gpt_academic_string_mask_langbased
from void_terminal.toolbox import build_gpt_academic_masked_string_langbased
from textwrap import dedent

def get_core_functions():
    return {

        "Academic text polishing": {
            # [1*] Prefix string，Will be added before your input。For example，Used to describe your requirements，such as translation, code interpretation, polishing, etc.。
            #      Just fill in a prompt string here，Here it`s a bit complicated to distinguish between Chinese and English contexts
            "Prefix":   build_gpt_academic_masked_string_langbased(
                            text_show_english=
                                r"Below is a paragraph from an academic paper. Polish the writing to meet the academic style, "
                                r"improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. "
                                r"Firstly, you should provide the polished paragraph. "
                                r"Secondly, you should list all your modification and explain the reasons to do so in markdown table.",
                            text_show_chinese=
                                r"As a Chinese academic paper writing improvement assistant，Your task is to improve the spelling, grammar, clarity, conciseness and overall readability of the provided text，"
                                r"Also, break down long sentences，Reduce repetition，And provide improvement suggestions。Please provide the corrected version of the text first，Then list the changes in a Markdown table，And provide reasons for the changes:"
                        ) + "\n\n",
            # [2*] Suffix string，Will be added after your input。For example，With the prefix, you can enclose your input content in quotation marks
            "Suffix":   r"",
            # [3] Button color (Optional parameters，Default secondary)
            "Color":    r"secondary",
            # [4] Is the button visible? (Optional parameters，Default True，Visible immediately)
            "Visible": True,
            # [5] Whether to clear history when triggered (Optional parameters，Default False，That is, do not process previous conversation history)
            "AutoClearHistory": False,
            # [6] Text preprocessing （Optional parameters，Default None，For example：Write a function to remove all line breaks）
            "PreProcess": None,
            # [7] Model selection （Optional parameters。If not set，Then use the current global model; if set，Then override the global model with the specified model。）
            # "ModelOverride": "gpt-3.5-turbo", # Main purpose：When forcing to click this basic function button，Use the specified model。
        },


        "Summarize mind mapping": {
            # Prefix，Will be added before your input。For example，Used to describe your requirements，such as translation, code interpretation, polishing, etc.
            "Prefix":   '''"""\n\n''',
            # Suffix，Will be added after your input。For example，With the prefix, you can enclose your input content in quotation marks
            "Suffix":
                # dedent() Function to remove indentation from multiline strings
                dedent("\n\n"+r'''
                    """

                    Summarize the above text using a mermaid flowchart，Summarize the content of the above paragraph and its inherent logical relationship，For example：

                    Below is a summary of the above text，Display in the form of a mermaid flowchart：
                    ```mermaid
                    flowchart LR
                        A["节点名1"] --> B("节点名2")
                        B --> C{"节点名3"}
                        C --> D["节点名4"]
                        C --> |"箭头名1"| E["节点名5"]
                        C --> |"箭头名2"| F["节点名6"]
                    ```

                    Attention：
                    （1）Use Chinese
                    （2）Node names should be enclosed in quotes， e.g., ["Laptop"]
                    （3）`|` and `"`No spaces between fields
                    （4）Choose flowchart LR based on the situation（From left to right）Or flowchart TD（From top to bottom）
                '''),
        },


        "Find syntax errors": {
            "Prefix":   r"Help me ensure that the grammar and the spelling is correct. "
                        r"Do not try to polish the text, if no mistake is found, tell me that this paragraph is good. "
                        r"If you find grammar or spelling mistakes, please list mistakes you find in a two-column markdown table, "
                        r"put the original text the first column, "
                        r"put the corrected text in the second column and highlight the key words you fixed. "
                        r"Finally, please provide the proofreaded text.""\n\n"
                        r"Example:""\n"
                        r"Paragraph: How is you? Do you knows what is it?""\n"
                        r"| Original sentence | Corrected sentence |""\n"
                        r"| :--- | :--- |""\n"
                        r"| How **is** you? | How **are** you? |""\n"
                        r"| Do you **knows** what **is** **it**? | Do you **know** what **it** **is** ? |""\n\n"
                        r"Below is a paragraph from an academic paper. "
                        r"You need to report all grammar and spelling mistakes as the example before."
                        + "\n\n",
            "Suffix":   r"",
            "PreProcess": clear_line_break,    # Preprocessing：Remove line breaks
        },


        "Chinese to English translation": {
            "Prefix":   r"Please translate following sentence to English:" + "\n\n",
            "Suffix":   r"",
        },


        "Academic English-Chinese Translation": {
            "Prefix":   build_gpt_academic_masked_string_langbased(
                            text_show_chinese=
                                r"I want you to act as a scientific English-Chinese translator, "
                                r"I will provide you with some paragraphs in one language "
                                r"and your task is to accurately and academically translate the paragraphs only into the other language. "
                                r"Do not repeat the original provided paragraphs after translation. "
                                r"You should use artificial intelligence tools, "
                                r"such as natural language processing, and rhetorical knowledge "
                                r"and experience about effective writing techniques to reply. "
                                r"I'll give you my paragraphs as follows, tell me what language it is written in, and then translate:",
                            text_show_english=
                                r"You Are an Experienced Translator，Please translate the following academic article paragraph into Chinese，"
                                r"And at the same time, fully consider Chinese grammar, clarity, conciseness, and overall readability，"
                                r"If necessary，You can change the order of the whole sentence to ensure that the translated paragraph is in line with Chinese language habits。"
                                r"The text you need to translate is as follows："
                        ) + "\n\n",
            "Suffix":   r"",
        },


        "English to Chinese translation": {
            "Prefix":   r"Translate into authentic Chinese：" + "\n\n",
            "Suffix":   r"",
            "Visible":  False,
        },


        "Find image": {
            "Prefix":   r"I need you to find a web image。Use Unsplash API(https://source.unsplash.com/960x640/?<English keywords>)Get image URL，"
                        r"Then please wrap it in Markdown format，And do not use backslashes，Do not use code blocks。Now，Please send me the image following the description below：" + "\n\n",
            "Suffix":   r"",
            "Visible":  False,
        },


        "Explain code": {
            "Prefix":   r"Please explain the following code：" + "\n```\n",
            "Suffix":   "\n```\n",
        },


        "Convert reference to Bib": {
            "Prefix":   r"Here are some bibliography items, please transform them into bibtex style."
                        r"Note that, reference styles maybe more than one kind, you should transform each item correctly."
                        r"Items need to be transformed:" + "\n\n",
            "Visible":  False,
            "Suffix":   r"",
        }
    }


def handle_core_functionality(additional_fn, inputs, history, chatbot):
    import core_functional
    importlib.reload(core_functional)    # Hot update prompt
    core_functional = core_functional.get_core_functions()
    addition = chatbot._cookies['customize_fn_overwrite']
    if additional_fn in addition:
        # Custom Function
        inputs = addition[additional_fn]["Prefix"] + inputs + addition[additional_fn]["Suffix"]
        return inputs, history
    else:
        # Prefabricated Function
        if "PreProcess" in core_functional[additional_fn]:
            if core_functional[additional_fn]["PreProcess"] is not None:
                inputs = core_functional[additional_fn]["PreProcess"](inputs)  # Get preprocessing function（If any）
        # Add the defined prefix and suffix to the string。
        inputs = apply_gpt_academic_string_mask_langbased(
            string = core_functional[additional_fn]["Prefix"] + inputs + core_functional[additional_fn]["Suffix"],
            lang_reference = inputs,
        )
        if core_functional[additional_fn].get("AutoClearHistory", False):
            history = []
        return inputs, history

if __name__ == "__main__":
    t = get_core_functions()["Summarize mind mapping"]
    print(t["Prefix"] + t["Suffix"])