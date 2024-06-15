import fake_gradio as gr

def define_gui_toolbar(AVAIL_LLM_MODELS, LLM_MODEL, INIT_SYS_PROMPT, THEME, AVAIL_THEMES, ADD_WAIFU, help_menu_description, js_code_for_toggle_darkmode):
    with gr.Floating(init_x="0%", init_y="0%", visible=True, width=None, drag="forbidden", elem_id="tooltip"):
        with gr.Row():
            with gr.Tab("Upload file", elem_id="interact-panel"):
                gr.Markdown("Please upload local files/zip packages for `Function Plugin Area` function call。Please note: After uploading the file, the input area will be automatically modified to the corresponding path。")
                file_upload_2 = gr.Files(label="Any file, Recommend Uploading Compressed File(zip, tar)", file_count="multiple", elem_id="elem_upload_float")

            with gr.Tab("Replace Model", elem_id="interact-panel"):
                md_dropdown = gr.Dropdown(AVAIL_LLM_MODELS, value=LLM_MODEL, elem_id="elem_model_sel", label="Change LLM model/request source").style(container=False)
                top_p = gr.Slider(minimum=-0, maximum=1.0, value=1.0, step=0.01,interactive=True, label="Top-p (nucleus sampling)",)
                temperature = gr.Slider(minimum=-0, maximum=2.0, value=1.0, step=0.01, interactive=True, label="Temperature", elem_id="elem_temperature")
                max_length_sl = gr.Slider(minimum=256, maximum=1024*32, value=4096, step=128, interactive=True, label="Local LLM MaxLength",)
                system_prompt = gr.Textbox(show_label=True, lines=2, placeholder=f"System Prompt", label="System prompt", value=INIT_SYS_PROMPT, elem_id="elem_prompt")
                temperature.change(None, inputs=[temperature], outputs=None,
                    _js="""(temperature)=>gpt_academic_gradio_saveload("save", "elem_prompt", "js_temperature_cookie", temperature)""")
                system_prompt.change(None, inputs=[system_prompt], outputs=None,
                    _js="""(system_prompt)=>gpt_academic_gradio_saveload("save", "elem_prompt", "js_system_prompt_cookie", system_prompt)""")
                md_dropdown.change(None, inputs=[md_dropdown], outputs=None,
                    _js="""(md_dropdown)=>gpt_academic_gradio_saveload("save", "elem_model_sel", "js_md_dropdown_cookie", md_dropdown)""")

            with gr.Tab("Interface appearance", elem_id="interact-panel"):
                theme_dropdown = gr.Dropdown(AVAIL_THEMES, value=THEME, label="Change UI theme").style(container=False)
                checkboxes = gr.CheckboxGroup(["Basic function area", "Function plugin area", "Floating input area", "Input clear key", "Plugin parameter area"], value=["Basic function area", "Function plugin area"], label="Show/hide function area", elem_id='cbs').style(container=False)
                opt = ["Custom menu"]
                value=[]
                if ADD_WAIFU: opt += ["Add Live2D image"]; value += ["Add Live2D image"]
                checkboxes_2 = gr.CheckboxGroup(opt, value=value, label="Show/Hide Custom Menu", elem_id='cbsc').style(container=False)
                dark_mode_btn = gr.Button("Switch interface brightness ☀", variant="secondary").style(size="sm")
                dark_mode_btn.click(None, None, None, _js=js_code_for_toggle_darkmode)
            with gr.Tab("Help", elem_id="interact-panel"):
                gr.Markdown(help_menu_description)
    return checkboxes, checkboxes_2, max_length_sl, theme_dropdown, system_prompt, file_upload_2, md_dropdown, top_p, temperature