import fake_gradio as gr
import json
from void_terminal.toolbox import format_io, find_free_port, on_file_uploaded, on_report_generated, get_conf, ArgsGeneralWrapper, DummyWith

def define_gui_advanced_plugin_class(plugins):
    # Define the advanced parameter area for the new generation of plugins
    with gr.Floating(init_x="50%", init_y="50%", visible=False, width="30%", drag="top", elem_id="plugin_arg_menu"):
        with gr.Accordion("Select plugin parameters", open=True, elem_id="plugin_arg_panel"):
            for u in range(8):
                with gr.Row():
                    gr.Textbox(show_label=True, label="T1", placeholder="Please enter", lines=1, visible=False, elem_id=f"plugin_arg_txt_{u}").style(container=False)
            for u in range(8):
                with gr.Row(): # PLUGIN_ARG_MENU
                    gr.Dropdown(label="T1", value="Please select", choices=[], visible=True, elem_id=f"plugin_arg_drop_{u}", interactive=True)

            with gr.Row():
                # This hidden textbox is responsible for loading the properties of the current pop-up plugin
                gr.Textbox(show_label=False, placeholder="Please enter", lines=1, visible=False,
                        elem_id=f"invisible_current_pop_up_plugin_arg").style(container=False)
                usr_confirmed_arg = gr.Textbox(show_label=False, placeholder="Please enter", lines=1, visible=False,
                        elem_id=f"invisible_current_pop_up_plugin_arg_final").style(container=False)

                arg_confirm_btn = gr.Button("Confirm parameters and execute", variant="stop")
                arg_confirm_btn.style(size="sm")

                arg_cancel_btn = gr.Button("Cancel", variant="stop")
                arg_cancel_btn.click(None, None, None, _js="""()=>close_current_pop_up_plugin()""")
                arg_cancel_btn.style(size="sm")

                arg_confirm_btn.click(None, None, None, _js="""()=>execute_current_pop_up_plugin()""")
                invisible_callback_btn_for_plugin_exe = gr.Button(r"No plugin selected", variant="secondary", visible=False, elem_id="invisible_callback_btn_for_plugin_exe").style(size="sm")
                # Registration of callback functions for dynamic buttons
                def route_switchy_bt_with_arg(request: gr.Request, input_order, *arg):
                    arguments = {k:v for k,v in zip(input_order, arg)}
                    which_plugin = arguments.pop('new_plugin_callback')
                    if which_plugin in [r"No plugin selected"]: return
                    usr_confirmed_arg = arguments.pop('usr_confirmed_arg')
                    arg_confirm: dict = {}
                    usr_confirmed_arg_dict = json.loads(usr_confirmed_arg)
                    for arg_name in usr_confirmed_arg_dict:
                        arg_confirm.update({arg_name: str(usr_confirmed_arg_dict[arg_name]['user_confirmed_value'])})
                    plugin_obj = plugins[which_plugin]["Class"]
                    arguments['plugin_advanced_arg'] = arg_confirm
                    if arg_confirm.get('main_input', None) is not None:
                        arguments['txt'] = arg_confirm['main_input']
                    yield from ArgsGeneralWrapper(plugin_obj.execute)(request, *arguments.values())
    return invisible_callback_btn_for_plugin_exe, route_switchy_bt_with_arg, usr_confirmed_arg

