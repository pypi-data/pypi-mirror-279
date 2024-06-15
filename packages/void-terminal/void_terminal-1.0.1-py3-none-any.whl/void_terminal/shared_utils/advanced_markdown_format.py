import markdown
import re
import os
import math
from textwrap import dedent
from functools import lru_cache
from pymdownx.superfences import fence_code_format
from latex2mathml.converter import convert as tex2mathml
from void_terminal.shared_utils.config_loader import get_conf as get_conf
from void_terminal.shared_utils.text_mask import apply_gpt_academic_string_mask

markdown_extension_configs = {
    "mdx_math": {
        "enable_dollar_delimiter": True,
        "use_gitlab_delimiters": False,
    },
}

code_highlight_configs = {
    "pymdownx.superfences": {
        "css_class": "codehilite",
        "custom_fences": [
            {"name": "mermaid", "class": "mermaid", "format": fence_code_format}
        ],
    },
    "pymdownx.highlight": {
        "css_class": "codehilite",
        "guess_lang": True,
        # 'auto_title': True,
        # 'linenums': True
    },
}

code_highlight_configs_block_mermaid = {
    "pymdownx.superfences": {
        "css_class": "codehilite",
        # "custom_fences": [
        #     {"name": "mermaid", "class": "mermaid", "format": fence_code_format}
        # ],
    },
    "pymdownx.highlight": {
        "css_class": "codehilite",
        "guess_lang": True,
        # 'auto_title': True,
        # 'linenums': True
    },
}

def tex2mathml_catch_exception(content, *args, **kwargs):
    try:
        content = tex2mathml(content, *args, **kwargs)
    except:
        content = content
    return content


def replace_math_no_render(match):
    content = match.group(1)
    if "mode=display" in match.group(0):
        content = content.replace("\n", "</br>")
        return f'<font color="#00FF00">$$</font><font color="#FF00FF">{content}</font><font color="#00FF00">$$</font>'
    else:
        return f'<font color="#00FF00">$</font><font color="#FF00FF">{content}</font><font color="#00FF00">$</font>'


def replace_math_render(match):
    content = match.group(1)
    if "mode=display" in match.group(0):
        if "\\begin{aligned}" in content:
            content = content.replace("\\begin{aligned}", "\\begin{array}")
            content = content.replace("\\end{aligned}", "\\end{array}")
            content = content.replace("&", " ")
        content = tex2mathml_catch_exception(content, display="block")
        return content
    else:
        return tex2mathml_catch_exception(content)


def markdown_bug_hunt(content):
    """
    Fix a bug in mdx_math（Redundant when wrapping begin command with single $<script>）
    """
    content = content.replace(
        '<script type="math/tex">\n<script type="math/tex; mode=display">',
        '<script type="math/tex; mode=display">',
    )
    content = content.replace("</script>\n</script>", "</script>")
    return content


def is_equation(txt):
    """
    Determine whether it is a formula | Test 1 write out the Lorentz law，Use the tex format formula to test 2 and give the Cauchy inequality，Write Maxwell`s equations using latex format for test 3
    """
    if "```" in txt and "```reference" not in txt:
        return False
    if "$" not in txt and "\\[" not in txt:
        return False
    mathpatterns = {
        r"(?<!\\|\$)(\$)([^\$]+)(\$)": {"allow_multi_lines": False},  #  $...$
        r"(?<!\\)(\$\$)([^\$]+)(\$\$)": {"allow_multi_lines": True},  # $$...$$
        r"(?<!\\)(\\\[)(.+?)(\\\])": {"allow_multi_lines": False},  # \[...\]
        # r'(?<!\\)(\\\()(.+?)(\\\))': {'allow_multi_lines': False},                       # \(...\)
        # r'(?<!\\)(\\begin{([a-z]+?\*?)})(.+?)(\\end{\2})': {'allow_multi_lines': True},  # \begin...\end
        # r'(?<!\\)(\$`)([^`]+)(`\$)': {'allow_multi_lines': False},                       # $`...`$
    }
    matches = []
    for pattern, property in mathpatterns.items():
        flags = re.ASCII | re.DOTALL if property["allow_multi_lines"] else re.ASCII
        matches.extend(re.findall(pattern, txt, flags))
    if len(matches) == 0:
        return False
    contain_any_eq = False
    illegal_pattern = re.compile(r"[^\x00-\x7F]|echo")
    for match in matches:
        if len(match) != 3:
            return False
        eq_canidate = match[1]
        if illegal_pattern.search(eq_canidate):
            return False
        else:
            contain_any_eq = True
    return contain_any_eq


def fix_markdown_indent(txt):
    # fix markdown indent
    if (" - " not in txt) or (". " not in txt):
        # do not need to fix, fast escape
        return txt
    # walk through the lines and fix non-standard indentation
    lines = txt.split("\n")
    pattern = re.compile(r"^\s+-")
    activated = False
    for i, line in enumerate(lines):
        if line.startswith("- ") or line.startswith("1. "):
            activated = True
        if activated and pattern.match(line):
            stripped_string = line.lstrip()
            num_spaces = len(line) - len(stripped_string)
            if (num_spaces % 4) == 3:
                num_spaces_should_be = math.ceil(num_spaces / 4) * 4
                lines[i] = " " * num_spaces_should_be + stripped_string
    return "\n".join(lines)


FENCED_BLOCK_RE = re.compile(
    dedent(
        r"""
        (?P<fence>^[ \t]*(?:~{3,}|`{3,}))[ ]*                      # opening fence
        ((\{(?P<attrs>[^\}\n]*)\})|                              # (optional {attrs} or
        (\.?(?P<lang>[\w#.+-]*)[ ]*)?                            # optional (.)lang
        (hl_lines=(?P<quot>"|')(?P<hl_lines>.*?)(?P=quot)[ ]*)?) # optional hl_lines)
        \n                                                       # newline (end of opening fence)
        (?P<code>.*?)(?<=\n)                                     # the code block
        (?P=fence)[ ]*$                                          # closing fence
    """
    ),
    re.MULTILINE | re.DOTALL | re.VERBOSE,
)


def get_line_range(re_match_obj, txt):
    start_pos, end_pos = re_match_obj.regs[0]
    num_newlines_before = txt[: start_pos + 1].count("\n")
    line_start = num_newlines_before
    line_end = num_newlines_before + txt[start_pos:end_pos].count("\n") + 1
    return line_start, line_end


def fix_code_segment_indent(txt):
    lines = []
    change_any = False
    txt_tmp = txt
    while True:
        re_match_obj = FENCED_BLOCK_RE.search(txt_tmp)
        if not re_match_obj:
            break
        if len(lines) == 0:
            lines = txt.split("\n")

        # Clear the location corresponding to txt_tmp for easier next search
        start_pos, end_pos = re_match_obj.regs[0]
        txt_tmp = txt_tmp[:start_pos] + " " * (end_pos - start_pos) + txt_tmp[end_pos:]
        line_start, line_end = get_line_range(re_match_obj, txt)

        # Get public indentation
        shared_indent_cnt = 1e5
        for i in range(line_start, line_end):
            stripped_string = lines[i].lstrip()
            num_spaces = len(lines[i]) - len(stripped_string)
            if num_spaces < shared_indent_cnt:
                shared_indent_cnt = num_spaces

        # Fix indentation
        if (shared_indent_cnt < 1e5) and (shared_indent_cnt % 4) == 3:
            num_spaces_should_be = math.ceil(shared_indent_cnt / 4) * 4
            for i in range(line_start, line_end):
                add_n = num_spaces_should_be - shared_indent_cnt
                lines[i] = " " * add_n + lines[i]
            if not change_any:  # Meet the first
                change_any = True

    if change_any:
        return "\n".join(lines)
    else:
        return txt


def markdown_convertion_for_file(txt):
    """
    Convert Markdown format text to HTML format。If it contains mathematical formulas，Convert the formula to HTML format first。
    """
    from void_terminal.themes.theme import advanced_css
    pre = f"""
    <!DOCTYPE html><head><meta charset="utf-8"><title>Conversation history</title><style>{advanced_css}</style></head>
    <body>
    <div class="test_temp1" style="width:10%; height: 500px; float:left;"></div>
    <div class="test_temp2" style="width:80%;padding: 40px;float:left;padding-left: 20px;padding-right: 20px;box-shadow: rgba(0, 0, 0, 0.2) 0px 0px 8px 8px;border-radius: 10px;">
        <div class="markdown-body">
    """
    suf = """
        </div>
    </div>
    <div class="test_temp3" style="width:10%; height: 500px; float:left;"></div>
    </body>
    """

    if txt.startswith(pre) and txt.endswith(suf):
        # print('Warning，Input a string that has already been converted，二次转化可能出Question')
        return txt  # Has already been converted，No need to convert again

    find_equation_pattern = r'<script type="math/tex(?:.*?)>(.*?)</script>'
    txt = fix_markdown_indent(txt)
    # convert everything to html format
    split = markdown.markdown(text="---")
    convert_stage_1 = markdown.markdown(
        text=txt,
        extensions=[
            "sane_lists",
            "tables",
            "mdx_math",
            "pymdownx.superfences",
            "pymdownx.highlight",
        ],
        extension_configs={**markdown_extension_configs, **code_highlight_configs},
    )
    convert_stage_1 = markdown_bug_hunt(convert_stage_1)

    # 2. convert to rendered equation
    convert_stage_2_2, n = re.subn(
        find_equation_pattern, replace_math_render, convert_stage_1, flags=re.DOTALL
    )
    # cat them together
    return pre + convert_stage_2_2 + suf

@lru_cache(maxsize=128)  # Use LRU cache to speed up conversion
def markdown_convertion(txt):
    """
    Convert Markdown format text to HTML format。If it contains mathematical formulas，Convert the formula to HTML format first。
    """
    pre = '<div class="markdown-body">'
    suf = "</div>"
    if txt.startswith(pre) and txt.endswith(suf):
        # print('Warning，Input a string that has already been converted，二次转化可能出Question')
        return txt  # Has already been converted，No need to convert again

    find_equation_pattern = r'<script type="math/tex(?:.*?)>(.*?)</script>'

    txt = fix_markdown_indent(txt)
    # txt = fix_code_segment_indent(txt)
    if is_equation(txt):  # Formula symbol with $ sign，And there is no code section```Identifier of
        # convert everything to html format
        split = markdown.markdown(text="---")
        convert_stage_1 = markdown.markdown(
            text=txt,
            extensions=[
                "sane_lists",
                "tables",
                "mdx_math",
                "pymdownx.superfences",
                "pymdownx.highlight",
            ],
            extension_configs={**markdown_extension_configs, **code_highlight_configs},
        )
        convert_stage_1 = markdown_bug_hunt(convert_stage_1)
        # 1. convert to easy-to-copy tex (do not render math)
        convert_stage_2_1, n = re.subn(
            find_equation_pattern,
            replace_math_no_render,
            convert_stage_1,
            flags=re.DOTALL,
        )
        # 2. convert to rendered equation
        convert_stage_2_2, n = re.subn(
            find_equation_pattern, replace_math_render, convert_stage_1, flags=re.DOTALL
        )
        # cat them together
        return pre + convert_stage_2_1 + f"{split}" + convert_stage_2_2 + suf
    else:
        return (
            pre
            + markdown.markdown(
                txt,
                extensions=[
                    "sane_lists",
                    "tables",
                    "pymdownx.superfences",
                    "pymdownx.highlight",
                ],
                extension_configs=code_highlight_configs,
            )
            + suf
        )


def close_up_code_segment_during_stream(gpt_reply):
    """
    In the middle of outputting code with GPT（Output the front part```，But haven`t output the back part yet```），Complete the back part```

    Args:
        gpt_reply (str): Reply string returned by GPT model。

    Returns:
        str: Return a new string，Append the back part of output code snippet```to it。

    """
    if "```" not in gpt_reply:
        return gpt_reply
    if gpt_reply.endswith("```"):
        return gpt_reply

    # Exclude the above two cases，We
    segments = gpt_reply.split("```")
    n_mark = len(segments) - 1
    if n_mark % 2 == 1:
        return gpt_reply + "\n```"  # Output code snippet!
    else:
        return gpt_reply


def special_render_issues_for_mermaid(text):
    # Handle a Mermaid Rendering Special Case in core_functional.py in an Ugly Way：
    # 我不希望"Summarize mind mapping"promptIn的mermaid渲染出来
    @lru_cache(maxsize=1)
    def get_special_case():
        from void_terminal.core_functional import get_core_functions
        special_case = get_core_functions()["Summarize mind mapping"]["Suffix"]
        return special_case
    if text.endswith(get_special_case()): text = text.replace("```mermaid", "```")
    return text


def compat_non_markdown_input(text):
    """
    Improve Display Effects for Non-Markdown Input，For example, converting spaces to &nbsp;，Convert line breaks to</br>etc.。
    """
    if "```" in text:
        # careful input：Markdown input
        text = special_render_issues_for_mermaid(text)  # Handle special rendering issues
        return text
    elif "</div>" in text:
        # careful input：HTML Input
        return text
    else:
        # whatever input：Non-markdown input
        lines = text.split("\n")
        for i, line in enumerate(lines):
            lines[i] = lines[i].replace(" ", "&nbsp;")  # Space Converted to &nbsp;;
        text = "</br>".join(lines)  # Convert line breaks to</br>
        return text


@lru_cache(maxsize=128)  # Use LRU caching
def simple_markdown_convertion(text):
    pre = '<div class="markdown-body">'
    suf = "</div>"
    if text.startswith(pre) and text.endswith(suf):
        return text  # Has already been converted，No need to convert again
    text = compat_non_markdown_input(text)    # Compatible with non-markdown input
    text = markdown.markdown(
        text,
        extensions=["pymdownx.superfences", "tables", "pymdownx.highlight"],
        extension_configs=code_highlight_configs,
    )
    return pre + text + suf


def format_io(self, y):
    """
    Parse input and output as HTML format。Paragraphize the input part of the last item in y，And convert the output part of Markdown and math formulas to HTML format。
    """
    if y is None or y == []:
        return []
    i_ask, gpt_reply = y[-1]
    i_ask = apply_gpt_academic_string_mask(i_ask, mode="show_render")
    gpt_reply = apply_gpt_academic_string_mask(gpt_reply, mode="show_render")
    # When the code output is halfway，Try to fill in the latter```
    if gpt_reply is not None:
        gpt_reply = close_up_code_segment_during_stream(gpt_reply)
    # Handle Questions and Outputs
    y[-1] = (
        # Input section
        None if i_ask is None else simple_markdown_convertion(i_ask),
        # Output section
        None if gpt_reply is None else markdown_convertion(gpt_reply),
    )
    return y
