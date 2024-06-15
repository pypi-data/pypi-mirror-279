from void_terminal.toolbox import CatchException, check_packages, get_conf
from void_terminal.toolbox import update_ui, update_ui_lastest_msg, disable_auto_promotion
from void_terminal.toolbox import trimmed_format_exc_markdown
from void_terminal.crazy_functions.crazy_utils import get_files_from_everything
from void_terminal.crazy_functions.pdf_fns.parse_pdf import get_avail_grobid_url
from void_terminal.crazy_functions.pdf_fns.parse_pdf_via_doc2x import ParsePDF_basedDOC2X
from void_terminal.crazy_functions.pdf_fns.parse_pdf_legacy import ParsePDF_simpleDecomposition
from void_terminal.crazy_functions.pdf_fns.parse_pdf_grobid import ParsePDF_BasedOnGROBID
from void_terminal.shared_utils.colorful import *

@CatchException
def BatchTranslatePDFDocuments(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):

    disable_auto_promotion(chatbot)
    # Basic information：Function, contributor
    chatbot.append([None, "Plugin function：BatchTranslatePDFDocuments。Function plugin contributor: Binary-Husky"])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
    try:
        check_packages(["fitz", "tiktoken", "scipdf"])
    except:
        chatbot.append([None, f"Failed to import software dependencies。Using this module requires additional dependencies，Installation method```pip install --upgrade pymupdf tiktoken scipdf_parser```。"])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Clear history，To avoid input overflow
    history = []
    success, file_manifest, project_folder = get_files_from_everything(txt, type='.pdf')

    # Checking input parameters，If no input parameters are given，Exit directly
    if (not success) and txt == "": txt = 'Empty input field。prompt：Please upload the file first（Drag the PDF file into the dialogue）。'

    # If no files are found
    if len(file_manifest) == 0:
        chatbot.append([None, f"Cannot find any file with .pdf extension: {txt}"])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # Start executing the task formally
    method = plugin_kwargs.get("pdf_parse_method", None)
    if method == "DOC2X":
        # ------- The first method，Best effect，But DOC2X service is required -------
        DOC2X_API_KEY = get_conf("DOC2X_API_KEY")
        if len(DOC2X_API_KEY) != 0:
            try:
                yield from ParsePDF_basedDOC2X(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, DOC2X_API_KEY, user_request)
                return
            except:
                chatbot.append([None, f"DOC2X service is not available，Now execute the older version code with slightly worse performance。{trimmed_format_exc_markdown()}"])
                yield from update_ui(chatbot=chatbot, history=history)

    if method == "GROBID":
        # ------- The second method，Effect is suboptimal -------
        grobid_url = get_avail_grobid_url()
        if grobid_url is not None:
            yield from ParsePDF_BasedOnGROBID(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, grobid_url)
            return

    if method == "ClASSIC":
        # ------- The third method，Early code，The effect is not ideal -------
        yield from update_ui_lastest_msg("GROBID service is unavailable，Please check the GROBID_URL in the config。As an alternative，Now execute the older version code with slightly worse performance。", chatbot, history, delay=3)
        yield from ParsePDF_simpleDecomposition(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)
        return

    if method is None:
        # ------- Try all three methods above once -------
        DOC2X_API_KEY = get_conf("DOC2X_API_KEY")
        if len(DOC2X_API_KEY) != 0:
            try:
                yield from ParsePDF_basedDOC2X(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, DOC2X_API_KEY, user_request)
                return
            except:
                chatbot.append([None, f"DOC2X service is not available，Trying GROBID。{trimmed_format_exc_markdown()}"])
                yield from update_ui(chatbot=chatbot, history=history)
        grobid_url = get_avail_grobid_url()
        if grobid_url is not None:
            yield from ParsePDF_BasedOnGROBID(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, grobid_url)
            return
        yield from update_ui_lastest_msg("GROBID service is unavailable，Please check the GROBID_URL in the config。As an alternative，Now execute the older version code with slightly worse performance。", chatbot, history, delay=3)
        yield from ParsePDF_simpleDecomposition(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)
        return

