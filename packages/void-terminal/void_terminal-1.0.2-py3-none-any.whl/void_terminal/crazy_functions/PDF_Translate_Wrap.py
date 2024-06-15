from void_terminal.crazy_functions.plugin_template.plugin_class_template import GptAcademicPluginTemplate, ArgProperty
from void_terminal.crazy_functions.PDF_Translate import BatchTranslatePDFDocuments


class PDF_Tran(GptAcademicPluginTemplate):
    def __init__(self):
        """
        Please note`execute`Will be executed in different threads，So when you define and use class variables，Should be extremely cautious!
        """
        pass

    def define_arg_selection_menu(self):
        """
        Define the secondary option menu of the plugin
        """
        gui_definition = {
            "main_input":
                ArgProperty(title="PDF file path", description="Path not specified，Please upload the file first，Click the plugin again", default_value="", type="string").model_dump_json(), # Primary input，Automatically sync from the input box
            "additional_prompt":
                ArgProperty(title="Additional prompt words", description="For example：Requirements for proper nouns, translation tone, etc.", default_value="", type="string").model_dump_json(), # Advanced parameter input area，automatic synchronization
            "pdf_parse_method":
                ArgProperty(title="PDF parsing method", options=["DOC2X", "GROBID", "ClASSIC"], description="None", default_value="GROBID", type="dropdown").model_dump_json(),
        }
        return gui_definition

    def execute(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
        """
        Execute the plugin
        """
        main_input = plugin_kwargs["main_input"]
        additional_prompt = plugin_kwargs["additional_prompt"]
        pdf_parse_method = plugin_kwargs["pdf_parse_method"]
        yield from BatchTranslatePDFDocuments(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request)