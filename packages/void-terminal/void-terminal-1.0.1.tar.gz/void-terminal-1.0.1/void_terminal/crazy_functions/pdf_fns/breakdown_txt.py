from void_terminal.crazy_functions.ipc_fns.mp import run_in_subprocess_with_timeout

def force_breakdown(txt, limit, get_token_fn):
    """ When punctuation and blank lines cannot be used for separation，We use the most brutal method to cut
    """
    for i in reversed(range(len(txt))):
        if get_token_fn(txt[:i]) < limit:
            return txt[:i], txt[i:]
    return "Tiktok unknown error", "Tiktok unknown error"


def maintain_storage(remain_txt_to_cut, remain_txt_to_cut_storage):
    """ To speed up calculations，We sample a special method。When remain_txt_to_cut > `_max` When， We save the text after _max to the remain_txt_to_cut_storage
    When remain_txt_to_cut < `_min` When，Then we extract part of the text from remain_txt_to_cut_storage
    """
    _min = int(5e4)
    _max = int(1e5)
    # print(len(remain_txt_to_cut), len(remain_txt_to_cut_storage))
    if len(remain_txt_to_cut) < _min and len(remain_txt_to_cut_storage) > 0:
        remain_txt_to_cut = remain_txt_to_cut + remain_txt_to_cut_storage
        remain_txt_to_cut_storage = ""
    if len(remain_txt_to_cut) > _max:
        remain_txt_to_cut_storage = remain_txt_to_cut[_max:] + remain_txt_to_cut_storage
        remain_txt_to_cut = remain_txt_to_cut[:_max]
    return remain_txt_to_cut, remain_txt_to_cut_storage


def cut(limit, get_token_fn, txt_tocut, must_break_at_empty_line, break_anyway=False):
    """ Text segmentation
    """
    res = []
    total_len = len(txt_tocut)
    fin_len = 0
    remain_txt_to_cut = txt_tocut
    remain_txt_to_cut_storage = ""
    # To speed up calculations，We sample a special method。When remain_txt_to_cut > `_max` When， We save the text after _max to the remain_txt_to_cut_storage
    remain_txt_to_cut, remain_txt_to_cut_storage = maintain_storage(remain_txt_to_cut, remain_txt_to_cut_storage)

    while True:
        if get_token_fn(remain_txt_to_cut) <= limit:
            # If the number of tokens in the remaining text is less than the limit，Then there`s no need to split
            res.append(remain_txt_to_cut); fin_len+=len(remain_txt_to_cut)
            break
        else:
            # If the number of remaining text tokens exceeds the limit，Then cut
            lines = remain_txt_to_cut.split('\n')

            # Estimate a split point
            estimated_line_cut = limit / get_token_fn(remain_txt_to_cut) * len(lines)
            estimated_line_cut = int(estimated_line_cut)

            # Start Looking for the Offset of an Appropriate Split Point（cnt）
            cnt = 0
            for cnt in reversed(range(estimated_line_cut)):
                if must_break_at_empty_line:
                    # Try using double empty lines first（\n\n）As a splitting point
                    if lines[cnt] != "":
                        continue
                prev = "\n".join(lines[:cnt])
                post = "\n".join(lines[cnt:])
                if get_token_fn(prev) < limit:
                    break

            if cnt == 0:
                # If no suitable splitting point is found
                if break_anyway:
                    # Whether to allow violent segmentation
                    prev, post = force_breakdown(remain_txt_to_cut, limit, get_token_fn)
                else:
                    # Direct error reporting is not allowed
                    raise RuntimeError(f"There is an extremely long line of text!{remain_txt_to_cut}")

            # Append list
            res.append(prev); fin_len+=len(prev)
            # Prepare for the next iteration
            remain_txt_to_cut = post
            remain_txt_to_cut, remain_txt_to_cut_storage = maintain_storage(remain_txt_to_cut, remain_txt_to_cut_storage)
            process = fin_len/total_len
            print(f'Text segmentation in progress {int(process*100)}%')
            if len(remain_txt_to_cut.strip()) == 0:
                break
    return res


def breakdown_text_to_satisfy_token_limit_(txt, limit, llm_model="gpt-3.5-turbo"):
    """ Attempt to split the text in various ways，To meet the token limit
    """
    from void_terminal.request_llms.bridge_all import model_info
    enc = model_info[llm_model]['tokenizer']
    def get_token_fn(txt): return len(enc.encode(txt, disallowed_special=()))
    try:
        # 1st attempt，Use double blank lines as splitting points（\n\n）As a splitting point
        return cut(limit, get_token_fn, txt, must_break_at_empty_line=True)
    except RuntimeError:
        try:
            # 2nd attempt，Use single blank lines（\n）As a splitting point
            return cut(limit, get_token_fn, txt, must_break_at_empty_line=False)
        except RuntimeError:
            try:
                # 3rd attempt，Use English periods（.）As a splitting point
                res = cut(limit, get_token_fn, txt.replace('.', '。\n'), must_break_at_empty_line=False) # This Chinese period is intentional，Exists as an identifier
                return [r.replace('。\n', '.') for r in res]
            except RuntimeError as e:
                try:
                    # 4th attempt，Chinese period（。）As a splitting point
                    res = cut(limit, get_token_fn, txt.replace('。', '。。\n'), must_break_at_empty_line=False)
                    return [r.replace('。。\n', '。') for r in res]
                except RuntimeError as e:
                    # 5th attempt，No other way，Just cut it randomly
                    return cut(limit, get_token_fn, txt, must_break_at_empty_line=False, break_anyway=True)

breakdown_text_to_satisfy_token_limit = run_in_subprocess_with_timeout(breakdown_text_to_satisfy_token_limit_, timeout=60)

if __name__ == '__main__':
    from void_terminal.crazy_functions.crazy_utils import read_and_clean_pdf_text
    file_content, page_one = read_and_clean_pdf_text("build/assets/at.pdf")

    from void_terminal.request_llms.bridge_all import model_info
    for i in range(5):
        file_content += file_content

    print(len(file_content))
    TOKEN_LIMIT_PER_FRAGMENT = 2500
    res = breakdown_text_to_satisfy_token_limit(file_content, TOKEN_LIMIT_PER_FRAGMENT)

