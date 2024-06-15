import re
from functools import lru_cache

# This code uses the re module in the Python programming language，That is, the regular expression library，Defined a regular expression pattern。
# This pattern is compiled into a regular expression object，Stored in a variable named const_extract_exp，To facilitate rapid matching and search operations later。
# Explanation of some special characters in regular expressions：
# - . represents any single character。
# - * means the previous character can appear 0 or more times。
# - ? Used here as a non-greedy match，That Is, It Will Match the Least Amount of Characters Possible。In(.*?)In，It ensures that any text we match is as short as possible，That is to say，It will be</show_llm>and</show_render>Stop matching before the label。
# - () Parentheses represent capture groups in regular expressions。
# - In this example，(.*?)Indicates Capturing Text of Arbitrary Length，Until the nearest qualifier outside the parentheses is encountered，That is</show_llm>and</show_render>。

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=/1=-=-=-=-=-=-=-=-=-=-=-=-=-=/2-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
const_extract_re = re.compile(
    r"<gpt_academic_string_mask><show_llm>(.*?)</show_llm><show_render>(.*?)</show_render></gpt_academic_string_mask>"
)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=/1=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-/2-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
const_extract_langbased_re = re.compile(
    r"<gpt_academic_string_mask><lang_english>(.*?)</lang_english><lang_chinese>(.*?)</lang_chinese></gpt_academic_string_mask>",
    flags=re.DOTALL,
)

@lru_cache(maxsize=128)
def apply_gpt_academic_string_mask(string, mode="show_all"):
    """
    When there is a mask tag in the string（<gpt_academic_string_mask><show_...>），Depending on who is intended to view the string（Large Model，Web rendering），Process the string，Return the processed string
    Schematic diagram：https://mermaid.live/edit#pako:eNqlkUtLw0AUhf9KuOta0iaTplkIPlpduFJwoZEwJGNbzItpita2O6tF8QGKogXFtwu7cSHiq3-mk_oznFR8IYLgrGbuOd9hDrcCpmcR0GDW9ubNPKaBMDauuwI_A9M6YN-3y0bODwxsYos4BdMoBrTg5gwHF-d0mBH6-vqFQe58ed5m9XPW2uteX3Tubrj0ljLYcwxxR3h1zB43WeMs3G19yEM9uapDMe_NG9i2dagKw1Fee4c1D9nGEbtc-5n6HbNtJ8IyHOs8tbs7V2HrlDX2w2Y7XD_5haHEtQiNsOwfMVa_7TzsvrWIuJGo02qTrdwLk9gukQylHv3Afv1ML270s-HZUndrmW1tdA-WfvbM_jMFYuAQ6uCCxVdciTJ1CPLEITpo_GphypeouzXuw6XAmyi7JmgBLZEYlHwLB2S4gHMUO-9DH7tTnvf1CVoFFkBLSOk4QmlRTqpIlaWUHINyNFXjaQWpCYRURUKiWovBYo8X4ymEJFlECQUpqaQkJmuvWygPpg
    """
    if not string:
        return string
    if "<gpt_academic_string_mask>" not in string: # No need to process
        return string

    if mode == "show_all":
        return string
    if mode == "show_llm":
        string = const_extract_re.sub(r"\1", string)
    elif mode == "show_render":
        string = const_extract_re.sub(r"\2", string)
    else:
        raise ValueError("Invalid mode")
    return string


@lru_cache(maxsize=128)
def build_gpt_academic_masked_string(text_show_llm="", text_show_render=""):
    """
    Depending on who is intended to view the string（Large Model，Web rendering），Generate a string with masked tags
    """
    return f"<gpt_academic_string_mask><show_llm>{text_show_llm}</show_llm><show_render>{text_show_render}</show_render></gpt_academic_string_mask>"


@lru_cache(maxsize=128)
def apply_gpt_academic_string_mask_langbased(string, lang_reference):
    """
    When there is a mask tag in the string（<gpt_academic_string_mask><lang_...>），According to the language，Select prompt words，Process the string，Return the processed string
    For example，If lang_reference is English，Then only display English prompts，Chinese Keywords Will Not Be Displayed
    For example：
        Input 1
            string = "Attention，The lang_reference text is：<gpt_academic_string_mask><lang_english>English</lang_english><lang_chinese>Chinese</lang_chinese></gpt_academic_string_mask>"
            lang_reference = "hello world"
        Output 1
            "Attention，The lang_reference text is：English"

        Input 2
            string = "Attention，The lang_reference text isChinese"   # Note that there is no mask tag here，So it will not be processed
            lang_reference = "hello world"
        Output 2
            "Attention，The lang_reference text isChinese"            # Return as is
    """

    if "<gpt_academic_string_mask>" not in string: # No need to process
        return string

    def contains_chinese(string):
        chinese_regex = re.compile(u'[\u4e00-\u9fff]+')
        return chinese_regex.search(string) is not None

    mode = "english" if not contains_chinese(lang_reference) else "chinese"
    if mode == "english":
        string = const_extract_langbased_re.sub(r"\1", string)
    elif mode == "chinese":
        string = const_extract_langbased_re.sub(r"\2", string)
    else:
        raise ValueError("Invalid mode")
    return string


@lru_cache(maxsize=128)
def build_gpt_academic_masked_string_langbased(text_show_english="", text_show_chinese=""):
    """
    According to the language，Select prompt words，Process the string，Return the processed string
    """
    return f"<gpt_academic_string_mask><lang_english>{text_show_english}</lang_english><lang_chinese>{text_show_chinese}</lang_chinese></gpt_academic_string_mask>"


if __name__ == "__main__":
    # Test
    input_string = (
        "Hello\n"
        + build_gpt_academic_masked_string(text_show_llm="mermaid", text_show_render="")
        + "Hello\n"
    )
    print(
        apply_gpt_academic_string_mask(input_string, "show_llm")
    )  # Should print the strings with 'abc' in place of the academic mask tags
    print(
        apply_gpt_academic_string_mask(input_string, "show_render")
    )  # Should print the strings with 'xyz' in place of the academic mask tags
