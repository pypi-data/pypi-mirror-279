from void_terminal.toolbox import get_log_folder
from void_terminal.toolbox import update_ui, promote_file_to_downloadzone
from void_terminal.toolbox import write_history_to_file, promote_file_to_downloadzone
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency
from void_terminal.crazy_functions.crazy_utils import read_and_clean_pdf_text
from void_terminal.shared_utils.colorful import *
import os

def ParsePDF_simpleDecomposition(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    """
    Attention：This function has been deprecated!! The new function is located at：crazy_functions/pdf_fns/parse_pdf.py
    """
    import copy
    TOKEN_LIMIT_PER_FRAGMENT = 1024
    generated_conclusion_files = []
    generated_html_files = []
    from void_terminal.crazy_functions.pdf_fns.report_gen_html import construct_html
    for index, fp in enumerate(file_manifest):
        # Read PDF file
        file_content, page_one = read_and_clean_pdf_text(fp)
        file_content = file_content.encode('utf-8', 'ignore').decode()   # avoid reading non-utf8 chars
        page_one = str(page_one).encode('utf-8', 'ignore').decode()      # avoid reading non-utf8 chars

        # Recursively split the PDF file
        from void_terminal.crazy_functions.pdf_fns.breakdown_txt import breakdown_text_to_satisfy_token_limit
        paper_fragments = breakdown_text_to_satisfy_token_limit(txt=file_content, limit=TOKEN_LIMIT_PER_FRAGMENT, llm_model=llm_kwargs['llm_model'])
        page_one_fragments = breakdown_text_to_satisfy_token_limit(txt=page_one, limit=TOKEN_LIMIT_PER_FRAGMENT//4, llm_model=llm_kwargs['llm_model'])

        # For better results，We strip the part after Introduction（If there is）
        paper_meta = page_one_fragments[0].split('introduction')[0].split('Introduction')[0].split('INTRODUCTION')[0]

        # Single line，Get article meta information
        paper_meta_info = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=f"The following is the basic information of an academic paper，Please extract the following six parts: `Title`, `Conference or Journal`, `Author`, `Abstract`, `Number`, `Author`s Email`。Please output in markdown format，Finally, translate the abstract into Chinese。Please extract：{paper_meta}",
            inputs_show_user=f"Please extract from{fp}Please extract basic information such as `Title` and `Conference or Journal` from。",
            llm_kwargs=llm_kwargs,
            chatbot=chatbot, history=[],
            sys_prompt="Your job is to collect information from materials。",
        )

        # Multi-threaded，Translation
        gpt_response_collection = yield from request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency(
            inputs_array=[
                f"You need to translate the following content：\n{frag}" for frag in paper_fragments],
            inputs_show_user_array=[f"\n---\n Original text： \n\n {frag.replace('#', '')}  \n---\n Translation：\n " for frag in paper_fragments],
            llm_kwargs=llm_kwargs,
            chatbot=chatbot,
            history_array=[[paper_meta] for _ in paper_fragments],
            sys_prompt_array=[
                "As an academic translator, please，be responsible for accurately translating academic papers into Chinese。Please translate every sentence in the article。" + plugin_kwargs.get("additional_prompt", "")
                for _ in paper_fragments],
            # max_workers=5  # Maximum parallel overload allowed by OpenAI
        )
        gpt_response_collection_md = copy.deepcopy(gpt_response_collection)
        # Organize the format of the report
        for i,k in enumerate(gpt_response_collection_md):
            if i%2==0:
                gpt_response_collection_md[i] = f"\n\n---\n\n ## Original text[{i//2}/{len(gpt_response_collection_md)//2}]： \n\n {paper_fragments[i//2].replace('#', '')}  \n\n---\n\n ## Translation[{i//2}/{len(gpt_response_collection_md)//2}]：\n "
            else:
                gpt_response_collection_md[i] = gpt_response_collection_md[i]
        final = ["I. Overview of the paper\n\n---\n\n", paper_meta_info.replace('# ', '### ') + '\n\n---\n\n', "II. Translation of the paper", ""]
        final.extend(gpt_response_collection_md)
        create_report_file_name = f"{os.path.basename(fp)}.trans.md"
        res = write_history_to_file(final, create_report_file_name)
        promote_file_to_downloadzone(res, chatbot=chatbot)

        # Update UI
        generated_conclusion_files.append(f'{get_log_folder()}/{create_report_file_name}')
        chatbot.append((f"{fp}Are you done?？", res))
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

        # write html
        try:
            ch = construct_html()
            orig = ""
            trans = ""
            gpt_response_collection_html = copy.deepcopy(gpt_response_collection)
            for i,k in enumerate(gpt_response_collection_html):
                if i%2==0:
                    gpt_response_collection_html[i] = paper_fragments[i//2].replace('#', '')
                else:
                    gpt_response_collection_html[i] = gpt_response_collection_html[i]
            final = ["Overview of the paper", paper_meta_info.replace('# ', '### '),  "II. Translation of the paper",  ""]
            final.extend(gpt_response_collection_html)
            for i, k in enumerate(final):
                if i%2==0:
                    orig = k
                if i%2==1:
                    trans = k
                    ch.add_row(a=orig, b=trans)
            create_report_file_name = f"{os.path.basename(fp)}.trans.html"
            generated_html_files.append(ch.save_file(create_report_file_name))
        except:
            from void_terminal.toolbox import trimmed_format_exc
            print('writing html result failed:', trimmed_format_exc())

    # Prepare for file download
    for pdf_path in generated_conclusion_files:
        # Rename file
        rename_file = f'Translation -{os.path.basename(pdf_path)}'
        promote_file_to_downloadzone(pdf_path, rename_file=rename_file, chatbot=chatbot)
    for html_path in generated_html_files:
        # Rename file
        rename_file = f'Translation -{os.path.basename(html_path)}'
        promote_file_to_downloadzone(html_path, rename_file=rename_file, chatbot=chatbot)
    chatbot.append(("Provide a list of output files", str(generated_conclusion_files + generated_html_files)))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page


