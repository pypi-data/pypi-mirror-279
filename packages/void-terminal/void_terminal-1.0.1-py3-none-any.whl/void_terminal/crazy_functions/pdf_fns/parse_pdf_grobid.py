import os
from void_terminal.toolbox import CatchException, report_exception, get_log_folder, gen_time_str, check_packages
from void_terminal.toolbox import update_ui, promote_file_to_downloadzone, update_ui_lastest_msg, disable_auto_promotion
from void_terminal.toolbox import write_history_to_file, promote_file_to_downloadzone, get_conf, extract_archive
from void_terminal.crazy_functions.pdf_fns.parse_pdf import parse_pdf, translate_pdf

def ParsePDF_BasedOnGROBID(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, grobid_url):
    import copy, json
    TOKEN_LIMIT_PER_FRAGMENT = 1024
    generated_conclusion_files = []
    generated_html_files = []
    DST_LANG = "Chinese"
    from void_terminal.crazy_functions.pdf_fns.report_gen_html import construct_html
    for index, fp in enumerate(file_manifest):
        chatbot.append(["Current progress：", f"Connecting to GROBID service，Please wait: {grobid_url}\nIf the waiting time is too long，Please modify GROBID_URL in the config，Can modify to local GROBID service。"]); yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        article_dict = parse_pdf(fp, grobid_url)
        grobid_json_res = os.path.join(get_log_folder(), gen_time_str() + "grobid.json")
        with open(grobid_json_res, 'w+', encoding='utf8') as f:
            f.write(json.dumps(article_dict, indent=4, ensure_ascii=False))
        promote_file_to_downloadzone(grobid_json_res, chatbot=chatbot)
        if article_dict is None: raise RuntimeError("ParsePDF failed，Please check if the PDF is damaged。")
        yield from translate_pdf(article_dict, llm_kwargs, chatbot, fp, generated_conclusion_files, TOKEN_LIMIT_PER_FRAGMENT, DST_LANG, plugin_kwargs=plugin_kwargs)
    chatbot.append(("Provide a list of output files", str(generated_conclusion_files + generated_html_files)))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page


