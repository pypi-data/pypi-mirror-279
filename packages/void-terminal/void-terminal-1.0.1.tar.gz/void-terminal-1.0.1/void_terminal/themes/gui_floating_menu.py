import fake_gradio as gr

def define_gui_floating_menu(customize_btns, functional, predefined_btns, cookies, web_cookie_cache):
    with gr.Floating(init_x="20%", init_y="50%", visible=False, width="40%", drag="top") as area_input_secondary:
        with gr.Accordion("Floating input area", open=True, elem_id="input-panel2"):
            with gr.Row() as row:
                row.style(equal_height=True)
                with gr.Column(scale=10):
                    txt2 = gr.Textbox(show_label=False, placeholder="Input question here.",
                                    elem_id='user_input_float', lines=8, label="Input area 2").style(container=False)
                with gr.Column(scale=1, min_width=40):
                    submitBtn2 = gr.Button("Submit", variant="primary"); submitBtn2.style(size="sm")
                    resetBtn2 = gr.Button("Reset", variant="secondary"); resetBtn2.style(size="sm")
                    stopBtn2 = gr.Button("Stop", variant="secondary"); stopBtn2.style(size="sm")
                    clearBtn2 = gr.Button("Clear", elem_id="elem_clear2", variant="secondary", visible=False); clearBtn2.style(size="sm")


    with gr.Floating(init_x="20%", init_y="50%", visible=False, width="40%", drag="top") as area_customize:
        with gr.Accordion("Custom menu", open=True, elem_id="edit-panel"):
            with gr.Row() as row:
                with gr.Column(scale=10):
                    AVAIL_BTN = [btn for btn in customize_btns.keys()] + [k for k in functional]
                    basic_btn_dropdown = gr.Dropdown(AVAIL_BTN, value="Custom button 1", label="Select a button in the Basic Function Area that needs to be customized").style(container=False)
                    basic_fn_title = gr.Textbox(show_label=False, placeholder="Enter the new button name", lines=1).style(container=False)
                    basic_fn_prefix = gr.Textbox(show_label=False, placeholder="Enter a new prompt prefix", lines=4).style(container=False)
                    basic_fn_suffix = gr.Textbox(show_label=False, placeholder="Enter a new prompt suffix", lines=4).style(container=False)
                with gr.Column(scale=1, min_width=70):
                    basic_fn_confirm = gr.Button("Confirm and save", variant="primary"); basic_fn_confirm.style(size="sm")
                    basic_fn_clean   = gr.Button("Restore default", variant="primary"); basic_fn_clean.style(size="sm")

                    from void_terminal.shared_utils.cookie_manager import assign_btn__fn_builder
                    assign_btn = assign_btn__fn_builder(customize_btns, predefined_btns, cookies, web_cookie_cache)
                    # update btn
                    h = basic_fn_confirm.click(assign_btn, [web_cookie_cache, cookies, basic_btn_dropdown, basic_fn_title, basic_fn_prefix, basic_fn_suffix],
                                            [web_cookie_cache, cookies, *customize_btns.values(), *predefined_btns.values()])
                    h.then(None, [web_cookie_cache], None, _js="""(web_cookie_cache)=>{setCookie("web_cookie_cache", web_cookie_cache, 365);}""")
                    # clean up btn
                    h2 = basic_fn_clean.click(assign_btn, [web_cookie_cache, cookies, basic_btn_dropdown, basic_fn_title, basic_fn_prefix, basic_fn_suffix, gr.State(True)],
                                            [web_cookie_cache, cookies, *customize_btns.values(), *predefined_btns.values()])
                    h2.then(None, [web_cookie_cache], None, _js="""(web_cookie_cache)=>{setCookie("web_cookie_cache", web_cookie_cache, 365);}""")
    return area_input_secondary, txt2, area_customize, submitBtn2, resetBtn2, clearBtn2, stopBtn2