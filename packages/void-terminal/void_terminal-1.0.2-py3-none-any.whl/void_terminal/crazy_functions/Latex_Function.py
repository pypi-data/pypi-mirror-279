from void_terminal.toolbox import update_ui, trimmed_format_exc, get_conf, get_log_folder, promote_file_to_downloadzone, check_repeat_upload, map_file_to_sha256
from void_terminal.toolbox import CatchException, report_exception, update_ui_lastest_msg, zip_result, gen_time_str
from functools import partial
import glob, os, requests, time, json, tarfile

pj = os.path.join
ARXIV_CACHE_DIR = os.path.expanduser(f"~/arxiv_cache/")


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- Utility function -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ProfessionalTerminologyDeclaration  = 'If the term "agent" is used in this section, it should be translated to "Intelligent agent". '
def switch_prompt(pfg, mode, more_requirement):
    """
    Generate prompts and system prompts based on the mode for proofreading or translating.
    Args:
    - pfg: Proofreader or Translator instance.
    - mode: A string specifying the mode, either 'proofread' or 'translate_zh'.

    Returns:
    - inputs_array: A list of strings containing prompts for users to respond to.
    - sys_prompt_array: A list of strings containing prompts for system prompts.
    """
    n_split = len(pfg.sp_file_contents)
    if mode == 'proofread_en':
        inputs_array = [r"Below is a section from an academic paper, proofread this section." +
                        r"Do not modify any latex command such as \section, \cite, \begin, \item and equations. " + more_requirement +
                        r"Answer me only with the revised text:" +
                        f"\n\n{frag}" for frag in pfg.sp_file_contents]
        sys_prompt_array = ["You are a professional academic paper writer." for _ in range(n_split)]
    elif mode == 'translate_zh':
        inputs_array = [
            r"Below is a section from an English academic paper, translate it into Chinese. " + more_requirement +
            r"Do not modify any latex command such as \section, \cite, \begin, \item and equations. " +
            r"Answer me only with the translated text:" +
            f"\n\n{frag}" for frag in pfg.sp_file_contents]
        sys_prompt_array = ["You are a professional translator." for _ in range(n_split)]
    else:
        assert False, "Unknown command"
    return inputs_array, sys_prompt_array


def desend_to_extracted_folder_if_exist(project_folder):
    """
    Descend into the extracted folder if it exists, otherwise return the original folder.

    Args:
    - project_folder: A string specifying the folder path.

    Returns:
    - A string specifying the path to the extracted folder, or the original folder if there is no extracted folder.
    """
    maybe_dir = [f for f in glob.glob(f'{project_folder}/*') if os.path.isdir(f)]
    if len(maybe_dir) == 0: return project_folder
    if maybe_dir[0].endswith('.extract'): return maybe_dir[0]
    return project_folder


def move_project(project_folder, arxiv_id=None):
    """
    Create a new work folder and copy the project folder to it.

    Args:
    - project_folder: A string specifying the folder path of the project.

    Returns:
    - A string specifying the path to the new work folder.
    """
    import shutil, time
    time.sleep(2)  # avoid time string conflict
    if arxiv_id is not None:
        new_workfolder = pj(ARXIV_CACHE_DIR, arxiv_id, 'workfolder')
    else:
        new_workfolder = f'{get_log_folder()}/{gen_time_str()}'
    try:
        shutil.rmtree(new_workfolder)
    except:
        pass

    # align subfolder if there is a folder wrapper
    items = glob.glob(pj(project_folder, '*'))
    items = [item for item in items if os.path.basename(item) != '__MACOSX']
    if len(glob.glob(pj(project_folder, '*.tex'))) == 0 and len(items) == 1:
        if os.path.isdir(items[0]): project_folder = items[0]

    shutil.copytree(src=project_folder, dst=new_workfolder)
    return new_workfolder


def arxiv_download(chatbot, history, txt, allow_cache=True):
    def check_cached_translation_pdf(arxiv_id):
        translation_dir = pj(ARXIV_CACHE_DIR, arxiv_id, 'translation')
        if not os.path.exists(translation_dir):
            os.makedirs(translation_dir)
        target_file = pj(translation_dir, 'translate_zh.pdf')
        if os.path.exists(target_file):
            promote_file_to_downloadzone(target_file, rename_file=None, chatbot=chatbot)
            target_file_compare = pj(translation_dir, 'comparison.pdf')
            if os.path.exists(target_file_compare):
                promote_file_to_downloadzone(target_file_compare, rename_file=None, chatbot=chatbot)
            return target_file
        return False

    def is_float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    if txt.startswith('https://arxiv.org/pdf/'):
        arxiv_id = txt.split('/')[-1]   # 2402.14207v2.pdf
        txt = arxiv_id.split('v')[0]  # 2402.14207

    if ('.' in txt) and ('/' not in txt) and is_float(txt):  # is arxiv ID
        txt = 'https://arxiv.org/abs/' + txt.strip()
    if ('.' in txt) and ('/' not in txt) and is_float(txt[:10]):  # is arxiv ID
        txt = 'https://arxiv.org/abs/' + txt[:10]

    if not txt.startswith('https://arxiv.org'):
        return txt, None    # Is a local file，Skip download

    # <-------------- inspect format ------------->
    chatbot.append([f"Detected arXiv document link", 'Attempting to download ...'])
    yield from update_ui(chatbot=chatbot, history=history)
    time.sleep(1)  # Refresh the page

    url_ = txt  # https://arxiv.org/abs/1707.06690

    if not txt.startswith('https://arxiv.org/abs/'):
        msg = f"Failed to parse arXiv URL, Expected format, for example: https://arxiv.org/abs/1707.06690。Obtained format in reality: {url_}。"
        yield from update_ui_lastest_msg(msg, chatbot=chatbot, history=history)  # Refresh the page
        return msg, None
    # <-------------- set format ------------->
    arxiv_id = url_.split('/abs/')[-1]
    if 'v' in arxiv_id: arxiv_id = arxiv_id[:10]
    cached_translation_pdf = check_cached_translation_pdf(arxiv_id)
    if cached_translation_pdf and allow_cache: return cached_translation_pdf, arxiv_id

    url_tar = url_.replace('/abs/', '/e-print/')
    translation_dir = pj(ARXIV_CACHE_DIR, arxiv_id, 'e-print')
    extract_dst = pj(ARXIV_CACHE_DIR, arxiv_id, 'extract')
    os.makedirs(translation_dir, exist_ok=True)

    # <-------------- download arxiv source file ------------->
    dst = pj(translation_dir, arxiv_id + '.tar')
    if os.path.exists(dst):
        yield from update_ui_lastest_msg("Calling cache", chatbot=chatbot, history=history)  # Refresh the page
    else:
        yield from update_ui_lastest_msg("Start downloading", chatbot=chatbot, history=history)  # Refresh the page
        proxies = get_conf('proxies')
        r = requests.get(url_tar, proxies=proxies)
        with open(dst, 'wb+') as f:
            f.write(r.content)
    # <-------------- extract file ------------->
    yield from update_ui_lastest_msg("Download complete", chatbot=chatbot, history=history)  # Refresh the page
    from void_terminal.toolbox import extract_archive
    extract_archive(file_path=dst, dest_dir=extract_dst)
    return extract_dst, arxiv_id


def pdf2tex_project(pdf_file_path, plugin_kwargs):
    if plugin_kwargs["method"] == "MATHPIX":
        # Mathpix API credentials
        app_id, app_key = get_conf('MATHPIX_APPID', 'MATHPIX_APPKEY')
        headers = {"app_id": app_id, "app_key": app_key}

        # Step 1: Send PDF file for processing
        options = {
            "conversion_formats": {"tex.zip": True},
            "math_inline_delimiters": ["$", "$"],
            "rm_spaces": True
        }

        response = requests.post(url="https://api.mathpix.com/v3/pdf",
                                headers=headers,
                                data={"options_json": json.dumps(options)},
                                files={"file": open(pdf_file_path, "rb")})

        if response.ok:
            pdf_id = response.json()["pdf_id"]
            print(f"PDF processing initiated. PDF ID: {pdf_id}")

            # Step 2: Check processing status
            while True:
                conversion_response = requests.get(f"https://api.mathpix.com/v3/pdf/{pdf_id}", headers=headers)
                conversion_data = conversion_response.json()

                if conversion_data["status"] == "completed":
                    print("PDF processing completed.")
                    break
                elif conversion_data["status"] == "error":
                    print("Error occurred during processing.")
                else:
                    print(f"Processing status: {conversion_data['status']}")
                    time.sleep(5)  # wait for a few seconds before checking again

            # Step 3: Save results to local files
            output_dir = os.path.join(os.path.dirname(pdf_file_path), 'mathpix_output')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            url = f"https://api.mathpix.com/v3/pdf/{pdf_id}.tex"
            response = requests.get(url, headers=headers)
            file_name_wo_dot = '_'.join(os.path.basename(pdf_file_path).split('.')[:-1])
            output_name = f"{file_name_wo_dot}.tex.zip"
            output_path = os.path.join(output_dir, output_name)
            with open(output_path, "wb") as output_file:
                output_file.write(response.content)
            print(f"tex.zip file saved at: {output_path}")

            import zipfile
            unzip_dir = os.path.join(output_dir, file_name_wo_dot)
            with zipfile.ZipFile(output_path, 'r') as zip_ref:
                zip_ref.extractall(unzip_dir)

            return unzip_dir

        else:
            print(f"Error sending PDF for processing. Status code: {response.status_code}")
            return None
    else:
        from void_terminal.crazy_functions.pdf_fns.parse_pdf_via_doc2x import ParsePDF_DOC2X_toLatex
        unzip_dir = ParsePDF_DOC2X_toLatex(pdf_file_path)
        return unzip_dir




# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Plugin Main Program 1 =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


@CatchException
def CorrectEnglishInLatexWithPDFComparison(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    # <-------------- information about this plugin ------------->
    chatbot.append(["Function plugin feature？",
                    "Correcting the entire Latex project, Compile to PDF using LaTeX and highlight the corrections。Function plugin contributor: Binary-Husky。Notes: Currently only supports GPT3.5/GPT4，Unknown conversion effect of other models。Currently, the best conversion effect for machine learning literature，Unknown conversion effect for other types of literature。Tested only on Windows system，Unknown performance on other operating systems。"])
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page

    # <-------------- more requirements ------------->
    if ("advanced_arg" in plugin_kwargs) and (plugin_kwargs["advanced_arg"] == ""): plugin_kwargs.pop("advanced_arg")
    more_req = plugin_kwargs.get("advanced_arg", "")
    _switch_prompt_ = partial(switch_prompt, more_requirement=more_req)

    # <-------------- check deps ------------->
    try:
        import glob, os, time, subprocess
        subprocess.Popen(['pdflatex', '-version'])
        from void_terminal.crazy_functions.latex_fns.latex_actions import DecomposeAndConvertLatex, CompileLatex
    except Exception as e:
        chatbot.append([f"Parsing project: {txt}",
                        f"Failed to execute the LaTeX command。Latex is not installed, Or not in the environment variable PATH。Installation method: https://tug.org/texlive/。Error message\n\n```\n\n{trimmed_format_exc()}\n\n```\n\n"])
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
        return

    # <-------------- clear history and read input ------------->
    history = []
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_exception(chatbot, history, a=f"Parsing project: {txt}", b=f"Cannot find local project or do not have access: {txt}")
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.tex', recursive=True)]
    if len(file_manifest) == 0:
        report_exception(chatbot, history, a=f"Parsing project: {txt}", b=f"Cannot find any .tex files: {txt}")
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
        return

    # <-------------- if is a zip/tar file ------------->
    project_folder = desend_to_extracted_folder_if_exist(project_folder)

    # <-------------- move latex project away from temp folder ------------->
    project_folder = move_project(project_folder, arxiv_id=None)

    # <-------------- if merge_translate_zh is already generated, skip gpt req ------------->
    if not os.path.exists(project_folder + '/merge_proofread_en.tex'):
        yield from DecomposeAndConvertLatex(file_manifest, project_folder, llm_kwargs, plugin_kwargs,
                                       chatbot, history, system_prompt, mode='proofread_en',
                                       switch_prompt=_switch_prompt_)

    # <-------------- compile PDF ------------->
    success = yield from CompileLatex(chatbot, history, main_file_original='merge',
                                   main_file_modified='merge_proofread_en',
                                   work_folder_original=project_folder, work_folder_modified=project_folder,
                                   work_folder=project_folder)

    # <-------------- zip PDF ------------->
    zip_res = zip_result(project_folder)
    if success:
        chatbot.append((f"Success!", 'Please check the results（Compressed file）...'))
        yield from update_ui(chatbot=chatbot, history=history);
        time.sleep(1)  # Refresh the page
        promote_file_to_downloadzone(file=zip_res, chatbot=chatbot)
    else:
        chatbot.append((f"Failed",
                        'Although PDF generation failed, But please check the results（Compressed file）, Contains a Tex document that has been translated, It is also readable, You can go to the Github Issue area, Use this compressed package + Conversation_To_File for feedback ...'))
        yield from update_ui(chatbot=chatbot, history=history);
        time.sleep(1)  # Refresh the page
        promote_file_to_downloadzone(file=zip_res, chatbot=chatbot)

    # <-------------- we are done ------------->
    return success


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Plugin Main Program 2 =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@CatchException
def TranslateChineseToEnglishInLatexAndRecompilePDF(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    # <-------------- information about this plugin ------------->
    chatbot.append([
        "Function plugin feature？",
        "Translate the entire Latex project, Generate Chinese PDF。Function plugin contributor: Binary-Husky。Notes: This plugin has best support for Windows，Must install using Docker on Linux，See the main README.md of the project for details。Currently only supports GPT3.5/GPT4，Unknown conversion effect of other models。Currently, the best conversion effect for machine learning literature，Unknown conversion effect for other types of literature。"])
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page

    # <-------------- more requirements ------------->
    if ("advanced_arg" in plugin_kwargs) and (plugin_kwargs["advanced_arg"] == ""): plugin_kwargs.pop("advanced_arg")
    more_req = plugin_kwargs.get("advanced_arg", "")
    no_cache = more_req.startswith("--no-cache")
    if no_cache: more_req.lstrip("--no-cache")
    allow_cache = not no_cache
    _switch_prompt_ = partial(switch_prompt, more_requirement=more_req)

    # <-------------- check deps ------------->
    try:
        import glob, os, time, subprocess
        subprocess.Popen(['pdflatex', '-version'])
        from void_terminal.crazy_functions.latex_fns.latex_actions import DecomposeAndConvertLatex, CompileLatex
    except Exception as e:
        chatbot.append([f"Parsing project: {txt}",
                        f"Failed to execute the LaTeX command。Latex is not installed, Or not in the environment variable PATH。Installation method: https://tug.org/texlive/。Error message\n\n```\n\n{trimmed_format_exc()}\n\n```\n\n"])
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
        return

    # <-------------- clear history and read input ------------->
    history = []
    try:
        txt, arxiv_id = yield from arxiv_download(chatbot, history, txt, allow_cache)
    except tarfile.ReadError as e:
        yield from update_ui_lastest_msg(
            "Unable to Automatically Download the LaTeX Source Code of the Paper，Please go to arXiv and open the paper download page，Click on other Formats，Then manually download the LaTeX source package by downloading the source。Next, call the local Latex translation plugin。",
            chatbot=chatbot, history=history)
        return

    if txt.endswith('.pdf'):
        report_exception(chatbot, history, a=f"Parsing project: {txt}", b=f"Found an already translated PDF document")
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
        return

    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_exception(chatbot, history, a=f"Parsing project: {txt}", b=f"Unable to find local project or unable to process: {txt}")
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
        return

    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.tex', recursive=True)]
    if len(file_manifest) == 0:
        report_exception(chatbot, history, a=f"Parsing project: {txt}", b=f"Cannot find any .tex files: {txt}")
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
        return

    # <-------------- if is a zip/tar file ------------->
    project_folder = desend_to_extracted_folder_if_exist(project_folder)

    # <-------------- move latex project away from temp folder ------------->
    project_folder = move_project(project_folder, arxiv_id)

    # <-------------- if merge_translate_zh is already generated, skip gpt req ------------->
    if not os.path.exists(project_folder + '/merge_translate_zh.tex'):
        yield from DecomposeAndConvertLatex(file_manifest, project_folder, llm_kwargs, plugin_kwargs,
                                       chatbot, history, system_prompt, mode='translate_zh',
                                       switch_prompt=_switch_prompt_)

    # <-------------- compile PDF ------------->
    success = yield from CompileLatex(chatbot, history, main_file_original='merge',
                                   main_file_modified='merge_translate_zh', mode='translate_zh',
                                   work_folder_original=project_folder, work_folder_modified=project_folder,
                                   work_folder=project_folder)

    # <-------------- zip PDF ------------->
    zip_res = zip_result(project_folder)
    if success:
        chatbot.append((f"Success!", 'Please check the results（Compressed file）...'))
        yield from update_ui(chatbot=chatbot, history=history);
        time.sleep(1)  # Refresh the page
        promote_file_to_downloadzone(file=zip_res, chatbot=chatbot)
    else:
        chatbot.append((f"Failed",
                        'Although PDF generation failed, But please check the results（Compressed file）, Contains a Tex document that has been translated, You can go to the Github Issue area, Use this compressed package for feedback。If the system is Linux，Please check system fonts（See Github wiki） ...'))
        yield from update_ui(chatbot=chatbot, history=history);
        time.sleep(1)  # Refresh the page
        promote_file_to_downloadzone(file=zip_res, chatbot=chatbot)

    # <-------------- we are done ------------->
    return success


#  =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- Plugin main program 3 -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@CatchException
def TranslatePDFToChineseAndRecompilePDF(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    # <-------------- information about this plugin ------------->
    chatbot.append([
        "Function plugin feature？",
        "Convert PDF to LaTeX project，Recompile into PDF after translating into Chinese。Function plugin contributor: Marroh。Notes: This plugin has best support for Windows，Must install using Docker on Linux，See the main README.md of the project for details。Currently only supports GPT3.5/GPT4，Unknown conversion effect of other models。Currently, the best conversion effect for machine learning literature，Unknown conversion effect for other types of literature。"])
    yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page

    # <-------------- more requirements ------------->
    if ("advanced_arg" in plugin_kwargs) and (plugin_kwargs["advanced_arg"] == ""): plugin_kwargs.pop("advanced_arg")
    more_req = plugin_kwargs.get("advanced_arg", "")
    no_cache = more_req.startswith("--no-cache")
    if no_cache: more_req.lstrip("--no-cache")
    allow_cache = not no_cache
    _switch_prompt_ = partial(switch_prompt, more_requirement=more_req)

    # <-------------- check deps ------------->
    try:
        import glob, os, time, subprocess
        subprocess.Popen(['pdflatex', '-version'])
        from void_terminal.crazy_functions.latex_fns.latex_actions import DecomposeAndConvertLatex, CompileLatex
    except Exception as e:
        chatbot.append([f"Parsing project: {txt}",
                        f"Failed to execute the LaTeX command。Latex is not installed, Or not in the environment variable PATH。Installation method: https://tug.org/texlive/。Error message\n\n```\n\n{trimmed_format_exc()}\n\n```\n\n"])
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
        return

    # <-------------- clear history and read input ------------->
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = 'Empty input field'
        report_exception(chatbot, history, a=f"Parsing project: {txt}", b=f"Unable to find local project or unable to process: {txt}")
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
        return

    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.pdf', recursive=True)]
    if len(file_manifest) == 0:
        report_exception(chatbot, history, a=f"Parsing project: {txt}", b=f"Cannot find any .pdf files: {txt}")
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
        return
    if len(file_manifest) != 1:
        report_exception(chatbot, history, a=f"Parsing project: {txt}", b=f"Does Not Support Processing Multiple PDF Files Simultaneously: {txt}")
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
        return

    if plugin_kwargs.get("method", "") == 'MATHPIX':
        app_id, app_key = get_conf('MATHPIX_APPID', 'MATHPIX_APPKEY')
        if len(app_id) == 0 or len(app_key) == 0:
            report_exception(chatbot, history, a="Missing MATHPIX_APPID and MATHPIX_APPKEY。", b=f"Please configure MATHPIX_APPID and MATHPIX_APPKEY")
            yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
            return
    if plugin_kwargs.get("method", "") == 'DOC2X':
        app_id, app_key = "", ""
        DOC2X_API_KEY = get_conf('DOC2X_API_KEY')
        if len(DOC2X_API_KEY) == 0:
            report_exception(chatbot, history, a="Missing DOC2X_API_KEY。", b=f"Please configure DOC2X_API_KEY")
            yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
            return

    hash_tag = map_file_to_sha256(file_manifest[0])

    # # <-------------- check repeated pdf ------------->
    # chatbot.append([f"Check if the PDF has been uploaded multiple times", "Checking..."])
    # yield from update_ui(chatbot=chatbot, history=history)
    # repeat, project_folder = check_repeat_upload(file_manifest[0], hash_tag)

    # if repeat:
    #     yield from update_ui_lastest_msg(f"Duplicate upload detected，Please check the results（Compressed file）...", chatbot=chatbot, history=history)
    #     try:
    #         translate_pdf = [f for f in glob.glob(f'{project_folder}/**/merge_translate_zh.pdf', recursive=True)][0]
    #         promote_file_to_downloadzone(translate_pdf, rename_file=None, chatbot=chatbot)
    #         comparison_pdf = [f for f in glob.glob(f'{project_folder}/**/comparison.pdf', recursive=True)][0]
    #         promote_file_to_downloadzone(comparison_pdf, rename_file=None, chatbot=chatbot)
    #         zip_res = zip_result(project_folder)
    #         promote_file_to_downloadzone(file=zip_res, chatbot=chatbot)
    #         return
    #     except:
    #         report_exception(chatbot, history, a=f"Parsing project: {txt}", b=f"Duplicate upload detected，But unable to find the relevant file")
    #         yield from update_ui(chatbot=chatbot, history=history)
    # else:
    #     yield from update_ui_lastest_msg(f"No duplicate uploads found", chatbot=chatbot, history=history)

    # <-------------- convert pdf into tex ------------->
    chatbot.append([f"Parsing project: {txt}", "Converting PDF to TeX project，Please be patient..."])
    yield from update_ui(chatbot=chatbot, history=history)
    project_folder = pdf2tex_project(file_manifest[0], plugin_kwargs)
    if project_folder is None:
        report_exception(chatbot, history, a=f"Parsing project: {txt}", b=f"PDF conversion to TeX project failed")
        yield from update_ui(chatbot=chatbot, history=history)
        return False

    # <-------------- translate latex file into Chinese ------------->
    yield from update_ui_lastest_msg("The TeX project is being translated into Chinese...", chatbot=chatbot, history=history)
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.tex', recursive=True)]
    if len(file_manifest) == 0:
        report_exception(chatbot, history, a=f"Parsing project: {txt}", b=f"Cannot find any .tex files: {txt}")
        yield from update_ui(chatbot=chatbot, history=history)  # Refresh the page
        return

    # <-------------- if is a zip/tar file ------------->
    project_folder = desend_to_extracted_folder_if_exist(project_folder)

    # <-------------- move latex project away from temp folder ------------->
    project_folder = move_project(project_folder)

    # <-------------- set a hash tag for repeat-checking ------------->
    with open(pj(project_folder, hash_tag + '.tag'), 'w') as f:
        f.write(hash_tag)
        f.close()


    # <-------------- if merge_translate_zh is already generated, skip gpt req ------------->
    if not os.path.exists(project_folder + '/merge_translate_zh.tex'):
        yield from DecomposeAndConvertLatex(file_manifest, project_folder, llm_kwargs, plugin_kwargs,
                                    chatbot, history, system_prompt, mode='translate_zh',
                                    switch_prompt=_switch_prompt_)

    # <-------------- compile PDF ------------->
    yield from update_ui_lastest_msg("Compiling the Translated Project .tex Project into PDF...", chatbot=chatbot, history=history)
    success = yield from CompileLatex(chatbot, history, main_file_original='merge',
                                main_file_modified='merge_translate_zh', mode='translate_zh',
                                work_folder_original=project_folder, work_folder_modified=project_folder,
                                work_folder=project_folder)

    # <-------------- zip PDF ------------->
    zip_res = zip_result(project_folder)
    if success:
        chatbot.append((f"Success!", 'Please check the results（Compressed file）...'))
        yield from update_ui(chatbot=chatbot, history=history);
        time.sleep(1)  # Refresh the page
        promote_file_to_downloadzone(file=zip_res, chatbot=chatbot)
    else:
        chatbot.append((f"Failed",
                        'Although PDF generation failed, But please check the results（Compressed file）, Contains a Tex document that has been translated, You can go to the Github Issue area, Use this compressed package for feedback。If the system is Linux，Please check system fonts（See Github wiki） ...'))
        yield from update_ui(chatbot=chatbot, history=history);
        time.sleep(1)  # Refresh the page
        promote_file_to_downloadzone(file=zip_res, chatbot=chatbot)

    # <-------------- we are done ------------->
    return success
