from void_terminal.crazy_functions.crazy_utils import read_and_clean_pdf_text, get_files_from_everything
import os
import re
def extract_text_from_files(txt, chatbot, history):
    """
    Search for pdf/md/word, retrieve text content, and return status and text

    Input parameter Args:
        chatbot: chatbot inputs and outputs （Handle of the user interface dialog window，Used for data flow visualization）
        history (list): List of chat history （History，List of conversation history）

    Output Returns:
        Check if the file exists(bool)
        final_result(list):Text content
        page_one(list):First Page Content/Summary
        file_manifest(list):File path
        excption(string):Information That Requires Manual Processing by Users,Keep it empty if there are no errors
    """

    final_result = []
    page_one = []
    file_manifest = []
    excption = ""

    if txt == "":
        final_result.append(txt)
        return False, final_result, page_one, file_manifest, excption   #Return the content of the input area directly if it is not a file

    #Find files in the input area content
    file_pdf,pdf_manifest,folder_pdf = get_files_from_everything(txt, '.pdf')
    file_md,md_manifest,folder_md = get_files_from_everything(txt, '.md')
    file_word,word_manifest,folder_word = get_files_from_everything(txt, '.docx')
    file_doc,doc_manifest,folder_doc = get_files_from_everything(txt, '.doc')

    if file_doc:
        excption = "word"
        return False, final_result, page_one, file_manifest, excption

    file_num = len(pdf_manifest) + len(md_manifest) + len(word_manifest)
    if file_num == 0:
        final_result.append(txt)
        return False, final_result, page_one, file_manifest, excption   #Return the content of the input area directly if it is not a file

    if file_pdf:
        try:    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
            import fitz
        except:
            excption = "pdf"
            return False, final_result, page_one, file_manifest, excption
        for index, fp in enumerate(pdf_manifest):
            file_content, pdf_one = read_and_clean_pdf_text(fp) # （try）cut PDF by sections
            file_content = file_content.encode('utf-8', 'ignore').decode()   # avoid reading non-utf8 chars
            pdf_one = str(pdf_one).encode('utf-8', 'ignore').decode()  # avoid reading non-utf8 chars
            final_result.append(file_content)
            page_one.append(pdf_one)
            file_manifest.append(os.path.relpath(fp, folder_pdf))

    if file_md:
        for index, fp in enumerate(md_manifest):
            with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                file_content = f.read()
            file_content = file_content.encode('utf-8', 'ignore').decode()
            headers = re.findall(r'^#\s(.*)$', file_content, re.MULTILINE)  #Next, extract the first/second-level headings in md as summaries
            if len(headers) > 0:
                page_one.append("\n".join(headers)) #Merge all headings,Split by Line Break
            else:
                page_one.append("")
            final_result.append(file_content)
            file_manifest.append(os.path.relpath(fp, folder_md))

    if file_word:
        try:    # Attempt to import dependencies，If dependencies are missing，Give installation suggestions
            from docx import Document
        except:
            excption = "word_pip"
            return False, final_result, page_one, file_manifest, excption
        for index, fp in enumerate(word_manifest):
            doc = Document(fp)
            file_content = '\n'.join([p.text for p in doc.paragraphs])
            file_content = file_content.encode('utf-8', 'ignore').decode()
            page_one.append(file_content[:200])
            final_result.append(file_content)
            file_manifest.append(os.path.relpath(fp, folder_word))

    return True, final_result, page_one, file_manifest, excption