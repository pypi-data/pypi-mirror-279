import os, json; os.environ['no_proxy'] = '*' # Avoid unexpected pollution caused by proxy networks

help_menu_description = \
"""Github source code is open source and updated[Address 🚀](https://github.com/binary-husky/gpt_academic),
Thanks to the enthusiastic[Developers ❤️](https://github.com/binary-husky/gpt_academic/graphs/contributors).
</br></br>Please refer to the FAQ for common questions[Project Wiki](https://github.com/binary-husky/gpt_academic/wiki),
If you encounter a bug, please go to[Bug Feedback](https://github.com/binary-husky/gpt_academic/issues).
</br></br>Instructions for normal conversation: 1. Enter question; 2. Click Submit
</br></br>Basic Function Area Usage Instructions: 1. Enter Text; 2. Click any button in the basic function area
</br></br>Instructions for function plugin area: 1. Enter path/question, Or upload a file; Click any function plugin area button
</br></br>VoidTerminal Usage Instructions: Click VoidTerminal, Then enter the command as prompted, Click VoidTerminal again
</br></br>How to save the conversation: Click the save current conversation button
</br></br>How to have a voice conversation: Please read the Wiki
</br></br>How to temporarily change API_KEY: Submit after entering temporary API_KEY in the input area（Invalid after webpage refresh）"""

def enable_log(PATH_LOGGING):
    import logging
    admin_log_path = os.path.join(PATH_LOGGING, "admin")
    os.makedirs(admin_log_path, exist_ok=True)
    log_dir = os.path.join(admin_log_path, "chat_secrets.log")
    try:logging.basicConfig(filename=log_dir, level=logging.INFO, encoding="utf-8", format="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    except:logging.basicConfig(filename=log_dir, level=logging.INFO,  format="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    # Disable logging output from the 'httpx' logger
    logging.getLogger("httpx").setLevel(logging.WARNING)
    print(f"All conversation records will be saved automatically in the local directory{log_dir}, Please pay attention to self-privacy protection!")

def main():
    import fake_gradio as gr
    if gr.__version__ not in ['3.32.9', '3.32.10']:
        raise ModuleNotFoundError("Use the built-in Gradio for the best experience! Please run `pip install -r requirements.txt` Command to install built-in Gradio and other dependencies, See details in requirements.txt.")
    from void_terminal.request_llms.bridge_all import predict
    from void_terminal.toolbox import format_io, find_free_port, on_file_uploaded, on_report_generated, get_conf, ArgsGeneralWrapper, DummyWith
    # We suggest you to copy a config_private.py file to keep your secrets, such as API and proxy URLs, from being accidentally uploaded to Github and seen by others., Such as API and proxy URLs
    proxies, WEB_PORT, LLM_MODEL, CONCURRENT_COUNT, AUTHENTICATION = get_conf('proxies', 'WEB_PORT', 'LLM_MODEL', 'CONCURRENT_COUNT', 'AUTHENTICATION')
    CHATBOT_HEIGHT, LAYOUT, AVAIL_LLM_MODELS, AUTO_CLEAR_TXT = get_conf('CHATBOT_HEIGHT', 'LAYOUT', 'AVAIL_LLM_MODELS', 'AUTO_CLEAR_TXT')
    ENABLE_AUDIO, AUTO_CLEAR_TXT, PATH_LOGGING, AVAIL_THEMES, THEME, ADD_WAIFU = get_conf('ENABLE_AUDIO', 'AUTO_CLEAR_TXT', 'PATH_LOGGING', 'AVAIL_THEMES', 'THEME', 'ADD_WAIFU')
    NUM_CUSTOM_BASIC_BTN, SSL_KEYFILE, SSL_CERTFILE = get_conf('NUM_CUSTOM_BASIC_BTN', 'SSL_KEYFILE', 'SSL_CERTFILE')
    DARK_MODE, INIT_SYS_PROMPT, ADD_WAIFU, TTS_TYPE = get_conf('DARK_MODE', 'INIT_SYS_PROMPT', 'ADD_WAIFU', 'TTS_TYPE')
    if LLM_MODEL not in AVAIL_LLM_MODELS: AVAIL_LLM_MODELS += [LLM_MODEL]

    # If WEB_PORT is -1, then a random port will be selected for WEB
    PORT = find_free_port() if WEB_PORT <= 0 else WEB_PORT
    from void_terminal.check_proxy import get_current_version
    from void_terminal.themes.theme import adjust_theme, advanced_css, theme_declaration, js_code_clear, js_code_reset, js_code_show_or_hide, js_code_show_or_hide_group2
    from void_terminal.themes.theme import js_code_for_css_changing, js_code_for_toggle_darkmode, js_code_for_persistent_cookie_init
    from void_terminal.themes.theme import load_dynamic_theme, to_cookie_str, from_cookie_str, assign_user_uuid
    title_html = f"<h1 align=\"center\">GPT academic optimization {get_current_version()}</h1>{theme_declaration}"

    # Dialogue, logging
    enable_log(PATH_LOGGING)

    # Some common functional modules
    from void_terminal.core_functional import get_core_functions
    functional = get_core_functions()

    # Advanced function plugins
    from void_terminal.crazy_functional import get_crazy_functions
    DEFAULT_FN_GROUPS = get_conf('DEFAULT_FN_GROUPS')
    plugins = get_crazy_functions()
    all_plugin_groups = list(set([g for _, plugin in plugins.items() for g in plugin['Group'].split('|')]))
    match_group = lambda tags, groups: any([g in groups for g in tags.split('|')])

    # Transformation of markdown text format
    gr.Chatbot.postprocess = format_io

    # Make some adjustments in appearance and color
    set_theme = adjust_theme()

    # Proxy and automatic update
    from void_terminal.check_proxy import check_proxy, auto_update, warm_up_modules
    proxy_info = check_proxy(proxies)

    gr_L1 = lambda: gr.Row().style()
    gr_L2 = lambda scale, elem_id: gr.Column(scale=scale, elem_id=elem_id, min_width=400)
    if LAYOUT == "TOP-DOWN":
        gr_L1 = lambda: DummyWith()
        gr_L2 = lambda scale, elem_id: gr.Row()
        CHATBOT_HEIGHT /= 2

    cancel_handles = []
    customize_btns = {}
    predefined_btns = {}
    from void_terminal.shared_utils.cookie_manager import make_cookie_cache, make_history_cache
    with gr.Blocks(title="GPT academic optimization", theme=set_theme, analytics_enabled=False, css=advanced_css) as app_block:
        gr.HTML(title_html)
        secret_css = gr.Textbox(visible=False, elem_id="secret_css")
        register_advanced_plugin_init_code_arr = ""

        cookies, web_cookie_cache = make_cookie_cache() # Define backend state（cookies）Front end（web_cookie_cache）Two brothers
        with gr_L1():
            with gr_L2(scale=2, elem_id="gpt-chat"):
                chatbot = gr.Chatbot(label=f"Current model：{LLM_MODEL}", elem_id="gpt-chatbot")
                if LAYOUT == "TOP-DOWN":  chatbot.style(height=CHATBOT_HEIGHT)
                history, history_cache, history_cache_update = make_history_cache() # Define backend state（history）Front end（history_cache）backend setter（history_cache_update）Three brothers
            with gr_L2(scale=1, elem_id="gpt-panel"):
                with gr.Accordion("Input area", open=True, elem_id="input-panel") as area_input_primary:
                    with gr.Row():
                        txt = gr.Textbox(show_label=False, placeholder="Input question here.", elem_id='user_input_main').style(container=False)
                    with gr.Row():
                        submitBtn = gr.Button("Submit", elem_id="elem_submit", variant="primary")
                    with gr.Row():
                        resetBtn = gr.Button("Reset", elem_id="elem_reset", variant="secondary"); resetBtn.style(size="sm")
                        stopBtn = gr.Button("Stop", elem_id="elem_stop", variant="secondary"); stopBtn.style(size="sm")
                        clearBtn = gr.Button("Clear", elem_id="elem_clear", variant="secondary", visible=False); clearBtn.style(size="sm")
                    if ENABLE_AUDIO:
                        with gr.Row():
                            audio_mic = gr.Audio(source="microphone", type="numpy", elem_id="elem_audio", streaming=True, show_label=False).style(container=False)
                    with gr.Row():
                        status = gr.Markdown(f"Tip: Submit by pressing Enter, Press Shift+Enter to line break。Current model: {LLM_MODEL} \n {proxy_info}", elem_id="state-panel")

                with gr.Accordion("Basic function area", open=True, elem_id="basic-panel") as area_basic_fn:
                    with gr.Row():
                        for k in range(NUM_CUSTOM_BASIC_BTN):
                            customize_btn = gr.Button("Custom button" + str(k+1), visible=False, variant="secondary", info_str=f'Basic function area: Custom button')
                            customize_btn.style(size="sm")
                            customize_btns.update({"Custom button" + str(k+1): customize_btn})
                        for k in functional:
                            if ("Visible" in functional[k]) and (not functional[k]["Visible"]): continue
                            variant = functional[k]["Color"] if "Color" in functional[k] else "secondary"
                            functional[k]["Button"] = gr.Button(k, variant=variant, info_str=f'Basic function area: {k}')
                            functional[k]["Button"].style(size="sm")
                            predefined_btns.update({k: functional[k]["Button"]})
                with gr.Accordion("Function plugin area", open=True, elem_id="plugin-panel") as area_crazy_fn:
                    with gr.Row():
                        gr.Markdown("<small>The plugin can read text/path in the input area as parameters（Automatically correct the path when uploading files）</small>")
                    with gr.Row(elem_id="input-plugin-group"):
                        plugin_group_sel = gr.Dropdown(choices=all_plugin_groups, label='', show_label=False, value=DEFAULT_FN_GROUPS,
                                                      multiselect=True, interactive=True, elem_classes='normal_mut_select').style(container=False)
                    with gr.Row():
                        for k, plugin in plugins.items():
                            if not plugin.get("AsButton", True): continue
                            visible = True if match_group(plugin['Group'], DEFAULT_FN_GROUPS) else False
                            variant = plugins[k]["Color"] if "Color" in plugin else "secondary"
                            info = plugins[k].get("Info", k)
                            plugin['Button'] = plugins[k]['Button'] = gr.Button(k, variant=variant,
                                visible=visible, info_str=f'Function plugin area: {info}').style(size="sm")
                    with gr.Row():
                        with gr.Accordion("More function plugins", open=True):
                            dropdown_fn_list = []
                            for k, plugin in plugins.items():
                                if not match_group(plugin['Group'], DEFAULT_FN_GROUPS): continue
                                if not plugin.get("AsButton", True): dropdown_fn_list.append(k)     # Exclude plugins that are already buttons
                                elif plugin.get('AdvancedArgs', False): dropdown_fn_list.append(k)  # For plugins that require advanced parameters，Also displayed in the dropdown menu
                            with gr.Row():
                                dropdown = gr.Dropdown(dropdown_fn_list, value=r"Click Here to Search the Plugin List", label="", show_label=False).style(container=False)
                            with gr.Row():
                                plugin_advanced_arg = gr.Textbox(show_label=True, label="Advanced parameter input area", visible=False, elem_id="advance_arg_input_legacy",
                                                                 placeholder="Here is the advanced parameter input area for special function plugins").style(container=False)
                            with gr.Row():
                                switchy_bt = gr.Button(r"Please select from the plugin list first", variant="secondary").style(size="sm")
                    with gr.Row():
                        with gr.Accordion("Click to Expand `File Download Area`。", open=False) as area_file_up:
                            file_upload = gr.Files(label="Any file, Recommend Uploading Compressed File(zip, tar)", file_count="multiple", elem_id="elem_upload")

        from void_terminal.themes.gui_toolbar import define_gui_toolbar
        checkboxes, checkboxes_2, max_length_sl, theme_dropdown, system_prompt, file_upload_2, md_dropdown, top_p, temperature = \
            define_gui_toolbar(AVAIL_LLM_MODELS, LLM_MODEL, INIT_SYS_PROMPT, THEME, AVAIL_THEMES, ADD_WAIFU, help_menu_description, js_code_for_toggle_darkmode)

        from void_terminal.themes.gui_floating_menu import define_gui_floating_menu
        area_input_secondary, txt2, area_customize, submitBtn2, resetBtn2, clearBtn2, stopBtn2 = \
            define_gui_floating_menu(customize_btns, functional, predefined_btns, cookies, web_cookie_cache)

        from void_terminal.themes.gui_advanced_plugin_class import define_gui_advanced_plugin_class
        new_plugin_callback, route_switchy_bt_with_arg, usr_confirmed_arg = \
            define_gui_advanced_plugin_class(plugins)

        # Interaction between display switch and function area
        def fn_area_visibility(a):
            ret = {}
            ret.update({area_input_primary: gr.update(visible=("Floating input area" not in a))})
            ret.update({area_input_secondary: gr.update(visible=("Floating input area" in a))})
            ret.update({plugin_advanced_arg: gr.update(visible=("Plugin parameter area" in a))})
            if "Floating input area" in a: ret.update({txt: gr.update(value="")})
            return ret
        checkboxes.select(fn_area_visibility, [checkboxes], [area_basic_fn, area_crazy_fn, area_input_primary, area_input_secondary, txt, txt2, plugin_advanced_arg] )
        checkboxes.select(None, [checkboxes], None, _js=js_code_show_or_hide)

        # Interaction between display switch and function area
        def fn_area_visibility_2(a):
            ret = {}
            ret.update({area_customize: gr.update(visible=("Custom menu" in a))})
            return ret
        checkboxes_2.select(fn_area_visibility_2, [checkboxes_2], [area_customize] )
        checkboxes_2.select(None, [checkboxes_2], None, _js=js_code_show_or_hide_group2)

        # Organize repeated control handle combinations
        input_combo = [cookies, max_length_sl, md_dropdown, txt, txt2, top_p, temperature, chatbot, history, system_prompt, plugin_advanced_arg]
        input_combo_order = ["cookies", "max_length_sl", "md_dropdown", "txt", "txt2", "top_p", "temperature", "chatbot", "history", "system_prompt", "plugin_advanced_arg"]
        output_combo = [cookies, chatbot, history, status]
        predict_args = dict(fn=ArgsGeneralWrapper(predict), inputs=[*input_combo, gr.State(True)], outputs=output_combo)
        # Submit button, reset button
        cancel_handles.append(txt.submit(**predict_args))
        cancel_handles.append(txt2.submit(**predict_args))
        cancel_handles.append(submitBtn.click(**predict_args))
        cancel_handles.append(submitBtn2.click(**predict_args))
        resetBtn.click(None, None, [chatbot, history, status], _js=js_code_reset)   # First, quickly clear chatbot & status in the frontend
        resetBtn2.click(None, None, [chatbot, history, status], _js=js_code_reset)  # First, quickly clear chatbot & status in the frontend
        reset_server_side_args = (lambda history: ([], [], "Reset", json.dumps(history)), [history], [chatbot, history, status, history_cache])
        resetBtn.click(*reset_server_side_args)    # Clear history on the backend again，Transfer history to history_cache for backup
        resetBtn2.click(*reset_server_side_args)   # Clear history on the backend again，Transfer history to history_cache for backup
        clearBtn.click(None, None, [txt, txt2], _js=js_code_clear)
        clearBtn2.click(None, None, [txt, txt2], _js=js_code_clear)
        if AUTO_CLEAR_TXT:
            submitBtn.click(None, None, [txt, txt2], _js=js_code_clear)
            submitBtn2.click(None, None, [txt, txt2], _js=js_code_clear)
            txt.submit(None, None, [txt, txt2], _js=js_code_clear)
            txt2.submit(None, None, [txt, txt2], _js=js_code_clear)
        # Registration of callback functions in basic function area
        for k in functional:
            if ("Visible" in functional[k]) and (not functional[k]["Visible"]): continue
            click_handle = functional[k]["Button"].click(fn=ArgsGeneralWrapper(predict), inputs=[*input_combo, gr.State(True), gr.State(k)], outputs=output_combo)
            cancel_handles.append(click_handle)
        for btn in customize_btns.values():
            click_handle = btn.click(fn=ArgsGeneralWrapper(predict), inputs=[*input_combo, gr.State(True), gr.State(btn.value)], outputs=output_combo)
            cancel_handles.append(click_handle)
        # File upload area，Interaction with chatbot after receiving files
        file_upload.upload(on_file_uploaded, [file_upload, chatbot, txt, txt2, checkboxes, cookies], [chatbot, txt, txt2, cookies]).then(None, None, None,   _js=r"()=>{toast_push('上传完毕 ...'); cancel_loading_status();}")
        file_upload_2.upload(on_file_uploaded, [file_upload_2, chatbot, txt, txt2, checkboxes, cookies], [chatbot, txt, txt2, cookies]).then(None, None, None, _js=r"()=>{toast_push('上传完毕 ...'); cancel_loading_status();}")
        # Function plugin - fixed button area
        for k in plugins:
            if plugins[k].get("Class", None):
                plugins[k]["JsMenu"] = plugins[k]["Class"]().get_js_code_for_generating_menu(k)
                register_advanced_plugin_init_code_arr += """register_advanced_plugin_init_code("{k}","{gui_js}");""".format(k=k, gui_js=plugins[k]["JsMenu"])
            if not plugins[k].get("AsButton", True): continue
            if plugins[k].get("Class", None) is None:
                assert plugins[k].get("Function", None) is not None
                click_handle = plugins[k]["Button"].click(ArgsGeneralWrapper(plugins[k]["Function"]), [*input_combo], output_combo)
                click_handle.then(on_report_generated, [cookies, file_upload, chatbot], [cookies, file_upload, chatbot]).then(None, [plugins[k]["Button"]], None, _js=r"(fn)=>on_plugin_exe_complete(fn)")
                cancel_handles.append(click_handle)
            else:
                click_handle = plugins[k]["Button"].click(None, inputs=[], outputs=None, _js=f"""()=>run_advanced_plugin_launch_code("{k}")""")

        # Interaction between dropdown menu and dynamic button in function plugin
        def on_dropdown_changed(k):
            variant = plugins[k]["Color"] if "Color" in plugins[k] else "secondary"
            info = plugins[k].get("Info", k)
            ret = {switchy_bt: gr.update(value=k, variant=variant, info_str=f'Function plugin area: {info}')}
            if plugins[k].get("AdvancedArgs", False): # Whether to call the advanced plugin parameter area
                ret.update({plugin_advanced_arg: gr.update(visible=True,  label=f"Plugin[{k}]Advanced parameter description for plugin：" + plugins[k].get("ArgsReminder", [f"No advanced parameter function description provided"]))})
            else:
                ret.update({plugin_advanced_arg: gr.update(visible=False, label=f"Plugin[{k}]No advanced parameters needed。")})
            return ret
        dropdown.select(on_dropdown_changed, [dropdown], [switchy_bt, plugin_advanced_arg] )

        def on_md_dropdown_changed(k):
            return {chatbot: gr.update(label="Current model："+k)}
        md_dropdown.select(on_md_dropdown_changed, [md_dropdown], [chatbot] )

        def on_theme_dropdown_changed(theme, secret_css):
            adjust_theme, css_part1, _, adjust_dynamic_theme = load_dynamic_theme(theme)
            if adjust_dynamic_theme:
                css_part2 = adjust_dynamic_theme._get_theme_css()
            else:
                css_part2 = adjust_theme()._get_theme_css()
            return css_part2 + css_part1

        theme_handle = theme_dropdown.select(on_theme_dropdown_changed, [theme_dropdown, secret_css], [secret_css])
        theme_handle.then(
            None,
            [secret_css],
            None,
            _js=js_code_for_css_changing
        )


        switchy_bt.click(None, [switchy_bt], None, _js="(switchy_bt)=>on_flex_button_click(switchy_bt)")
        # Registration of callback functions for dynamic buttons
        def route(request: gr.Request, k, *args, **kwargs):
            if k not in [r"Click Here to Search the Plugin List", r"Please select from the plugin list first"]:
                if plugins[k].get("Class", None) is None:
                    assert plugins[k].get("Function", None) is not None
                    yield from ArgsGeneralWrapper(plugins[k]["Function"])(request, *args, **kwargs)
        # Confirm button in the advanced parameter area of the old plugin（Hide）
        old_plugin_callback = gr.Button(r"No plugin selected", variant="secondary", visible=False, elem_id="old_callback_btn_for_plugin_exe")
        click_handle_ng = old_plugin_callback.click(route, [switchy_bt, *input_combo], output_combo)
        click_handle_ng.then(on_report_generated, [cookies, file_upload, chatbot], [cookies, file_upload, chatbot]).then(None, [switchy_bt], None, _js=r"(fn)=>on_plugin_exe_complete(fn)")
        cancel_handles.append(click_handle_ng)
        # Confirmation button for the advanced parameter area of the new generation plugin（Hide）
        click_handle_ng = new_plugin_callback.click(route_switchy_bt_with_arg, [
                gr.State(["new_plugin_callback", "usr_confirmed_arg"] + input_combo_order),
                new_plugin_callback, usr_confirmed_arg, *input_combo
            ], output_combo)
        click_handle_ng.then(on_report_generated, [cookies, file_upload, chatbot], [cookies, file_upload, chatbot]).then(None, [switchy_bt], None, _js=r"(fn)=>on_plugin_exe_complete(fn)")
        cancel_handles.append(click_handle_ng)
        # Callback function registration for the stop button
        stopBtn.click(fn=None, inputs=None, outputs=None, cancels=cancel_handles)
        stopBtn2.click(fn=None, inputs=None, outputs=None, cancels=cancel_handles)
        plugins_as_btn = {name:plugin for name, plugin in plugins.items() if plugin.get('Button', None)}
        def on_group_change(group_list):
            btn_list = []
            fns_list = []
            if not group_list: # Handling special cases：No plugin group selected
                return [*[plugin['Button'].update(visible=False) for _, plugin in plugins_as_btn.items()], gr.Dropdown.update(choices=[])]
            for k, plugin in plugins.items():
                if plugin.get("AsButton", True):
                    btn_list.append(plugin['Button'].update(visible=match_group(plugin['Group'], group_list))) # Refresh button
                    if plugin.get('AdvancedArgs', False): dropdown_fn_list.append(k) # For plugins that require advanced parameters，Also displayed in the dropdown menu
                elif match_group(plugin['Group'], group_list): fns_list.append(k) # Refresh the drop-down list
            return [*btn_list, gr.Dropdown.update(choices=fns_list)]
        plugin_group_sel.select(fn=on_group_change, inputs=[plugin_group_sel], outputs=[*[plugin['Button'] for name, plugin in plugins_as_btn.items()], dropdown])
        if ENABLE_AUDIO:
            from void_terminal.crazy_functions.live_audio.audio_io import RealtimeAudioDistribution
            rad = RealtimeAudioDistribution()
            def deal_audio(audio, cookies):
                rad.feed(cookies['uuid'].hex, audio)
            audio_mic.stream(deal_audio, inputs=[audio_mic, cookies])


        app_block.load(assign_user_uuid, inputs=[cookies], outputs=[cookies])

        from void_terminal.shared_utils.cookie_manager import load_web_cookie_cache__fn_builder
        load_web_cookie_cache = load_web_cookie_cache__fn_builder(customize_btns, cookies, predefined_btns)
        app_block.load(load_web_cookie_cache, inputs = [web_cookie_cache, cookies],
            outputs = [web_cookie_cache, cookies, *customize_btns.values(), *predefined_btns.values()], _js=js_code_for_persistent_cookie_init)

        app_block.load(None, inputs=[], outputs=None, _js=f"""()=>GptAcademicJavaScriptInit("{DARK_MODE}","{INIT_SYS_PROMPT}","{ADD_WAIFU}","{LAYOUT}","{TTS_TYPE}")""")    # Configure dark theme or light theme
        app_block.load(None, inputs=[], outputs=None, _js="""()=>{REP}""".replace("REP", register_advanced_plugin_init_code_arr))

    # In-browser triggering of gradio is not very stable，Roll back code to the original browser open function
    def run_delayed_tasks():
        import threading, webbrowser, time
        print(f"If the browser does not open automatically，Please copy and go to the following URL：")
        if DARK_MODE:   print(f"\tDark theme enabled（Support dynamic theme switching）」: http://localhost:{PORT}")
        else:           print(f"\tLight theme enabled（Support dynamic theme switching）」: http://localhost:{PORT}")

        def auto_updates(): time.sleep(0); auto_update()
        def open_browser(): time.sleep(2); webbrowser.open_new_tab(f"http://localhost:{PORT}")
        def warm_up_mods(): time.sleep(6); warm_up_modules()

        threading.Thread(target=auto_updates, name="self-upgrade", daemon=True).start() # Check for automatic updates
        threading.Thread(target=warm_up_mods, name="warm-up",      daemon=True).start() # Preheat the tiktoken module
        if get_conf('AUTO_OPEN_BROWSER'):
            threading.Thread(target=open_browser, name="open-browser", daemon=True).start() # Open browser page

    # Run some asynchronous tasks：Auto-update, open browser page, warm up tiktoken module
    run_delayed_tasks()

    # Finally，Officially start the service
    from void_terminal.shared_utils.fastapi_server import start_app
    start_app(app_block, CONCURRENT_COUNT, AUTHENTICATION, PORT, SSL_KEYFILE, SSL_CERTFILE)


if __name__ == "__main__":
    main()
