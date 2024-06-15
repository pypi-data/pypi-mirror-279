from void_terminal.toolbox import CatchException, update_ui, ProxyNetworkActivate, update_ui_lastest_msg, get_log_folder, get_user
from void_terminal.crazy_functions.crazy_utils import request_gpt_model_in_new_thread_with_ui_alive, get_files_from_everything

install_msg ="""

1. python -m pip install torch --index-url https://download.pytorch.org/whl/cpu

2. python -m pip install transformers protobuf langchain sentence-transformers  faiss-cpu nltk beautifulsoup4 bitsandbytes tabulate icetk --upgrade

3. python -m pip install unstructured[all-docs] --upgrade

4. python -c 'import nltk; nltk.download("punkt")'
"""

@CatchException
def InjectKnowledgeBaseFiles(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
    """
    txt             Text entered by the user in the input field，For example, a paragraph that needs to be translated，For example, a file path that contains files to be processed
    llm_kwargs      GPT model parameters, Such as temperature and top_p, Generally pass it on as is
    plugin_kwargs   Plugin model parameters，No use for the time being
    chatbot         Chat display box handle，Displayed to the user
    history         Chat history，Context summary
    system_prompt   Silent reminder to GPT
    user_request    Current user`s request information（IP addresses, etc.）
    """
    history = []    # Clear history，To avoid input overflow

    # < -------------------- Read parameters--------------- >
    if ("advanced_arg" in plugin_kwargs) and (plugin_kwargs["advanced_arg"] == ""): plugin_kwargs.pop("advanced_arg")
    kai_id = plugin_kwargs.get("advanced_arg", 'default')

    chatbot.append((f"To`{kai_id}`Add files to the knowledge base。", "[Local Message] From a batch of files(txt, md, tex)Build a knowledge base by reading data in, And then perform question-answering。"))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page

    # resolve deps
    try:
        # from zh_langchain import construct_vector_store
        # from langchain.embeddings.huggingface import HuggingFaceEmbeddings
        from void_terminal.crazy_functions.vector_fns.vector_database import knowledge_archive_interface
    except Exception as e:
        chatbot.append(["Insufficient dependencies", f"{str(e)}\n\nFailed to import dependencies。Please install with the following command" + install_msg])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        # from .crazy_utils import try_install_deps
        # try_install_deps(['zh_langchain==0.2.1', 'pypinyin'], reload_m=['pypinyin', 'zh_langchain'])
        # yield from update_ui_lastest_msg("Installation completed，You can try again。", chatbot, history)
        return

    # < --------------------Read the file--------------- >
    file_manifest = []
    spl = ["txt", "doc", "docx", "email", "epub", "html", "json", "md", "msg", "pdf", "ppt", "pptx", "rtf"]
    for sp in spl:
        _, file_manifest_tmp, _ = get_files_from_everything(txt, type=f'.{sp}')
        file_manifest += file_manifest_tmp

    if len(file_manifest) == 0:
        chatbot.append(["No readable files found", "Currently supported formats include: txt, md, docx, pptx, pdf, JSON, etc."])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        return

    # < ------------------- Preheating text vectorization module--------------- >
    chatbot.append(['<br/>'.join(file_manifest), "Preheating text vectorization module, If it is the first time running, Downloading Chinese vectorization model will take a long time..."])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
    print('Checking Text2vec ...')
    from langchain.embeddings.huggingface import HuggingFaceEmbeddings
    with ProxyNetworkActivate('Download_LLM'):    # Temporarily activate proxy network
        HuggingFaceEmbeddings(model_name="GanymedeNil/text2vec-large-chinese")

    # < ------------------Build knowledge base--------------- >
    chatbot.append(['<br/>'.join(file_manifest), "Building knowledge base..."])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
    print('Establishing knowledge archive ...')
    with ProxyNetworkActivate('Download_LLM'):    # Temporarily activate proxy network
        kai = knowledge_archive_interface()
        vs_path = get_log_folder(user=get_user(chatbot), plugin_name='vec_store')
        kai.feed_archive(file_manifest=file_manifest, vs_path=vs_path, id=kai_id)
    kai_files = kai.get_loaded_file(vs_path=vs_path)
    kai_files = '<br/>'.join(kai_files)
    # chatbot.append(['Knowledge base构建成功', "正InConvertKnowledge base存储至cookieIn"])
    # yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
    # chatbot._cookies['langchain_plugin_embedding'] = kai.get_current_archive_id()
    # chatbot._cookies['lock_plugin'] = 'crazy_functions.InjectKnowledgeBaseFiles->ReadKnowledgeArchiveAnswerQuestions'
    # chatbot.append(['Completed', "“根据Knowledge base作Answer”function plugin已经接管AskAnswerSystem, Ask questions! But be careful, You can no longer use other plugins next，Refresh the page to exit UpdateKnowledgeArchive mode。"])
    chatbot.append(['Build completed', f"Valid files in the current knowledge base：\n\n---\n\n{kai_files}\n\n---\n\nPlease switch to the `UpdateKnowledgeArchive` plugin for knowledge base access, Or use this plugin to continue uploading more files。"])
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # As requesting GPT takes some time，Let`s do a UI update in time

@CatchException
def ReadKnowledgeArchiveAnswerQuestions(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request=-1):
    # resolve deps
    try:
        # from zh_langchain import construct_vector_store
        # from langchain.embeddings.huggingface import HuggingFaceEmbeddings
        from void_terminal.crazy_functions.vector_fns.vector_database import knowledge_archive_interface
    except Exception as e:
        chatbot.append(["Insufficient dependencies", f"{str(e)}\n\nFailed to import dependencies。Please install with the following command" + install_msg])
        yield from update_ui(chatbot=chatbot, history=history) # Refresh the page
        # from .crazy_utils import try_install_deps
        # try_install_deps(['zh_langchain==0.2.1', 'pypinyin'], reload_m=['pypinyin', 'zh_langchain'])
        # yield from update_ui_lastest_msg("Installation completed，You can try again。", chatbot, history)
        return

    # < -------------------  --------------- >
    kai = knowledge_archive_interface()

    if ("advanced_arg" in plugin_kwargs) and (plugin_kwargs["advanced_arg"] == ""): plugin_kwargs.pop("advanced_arg")
    kai_id = plugin_kwargs.get("advanced_arg", 'default')
    vs_path = get_log_folder(user=get_user(chatbot), plugin_name='vec_store')
    resp, prompt = kai.answer_with_archive_by_id(txt, kai_id, vs_path)

    chatbot.append((txt, f'[Knowledge base {kai_id}] ' + prompt))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # As requesting GPT takes some time，Let`s do a UI update in time
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=prompt, inputs_show_user=txt,
        llm_kwargs=llm_kwargs, chatbot=chatbot, history=[],
        sys_prompt=system_prompt
    )
    history.extend((prompt, gpt_say))
    yield from update_ui(chatbot=chatbot, history=history) # Refresh the page # As requesting GPT takes some time，Let`s do a UI update in time
