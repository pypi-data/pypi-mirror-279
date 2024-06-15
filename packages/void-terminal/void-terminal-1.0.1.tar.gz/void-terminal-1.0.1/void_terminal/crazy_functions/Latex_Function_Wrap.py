
from void_terminal.crazy_functions.Latex_Function import TranslateChineseToEnglishInLatexAndRecompilePDF, TranslatePDFToChineseAndRecompilePDF
from void_terminal.crazy_functions.plugin_template.plugin_class_template import GptAcademicPluginTemplate, ArgProperty


class Arxiv_Localize(GptAcademicPluginTemplate):
    def __init__(self):
        """
        Please note`execute`Will be executed in different threads，So when you define and use class variables，Should be extremely cautious!
        """
        pass

    def define_arg_selection_menu(self):
        """
        Define the secondary option menu of the plugin

        The first parameter，Name`main_input`，Parameters`type`Declare this as a text box，Displayed above the text box`title`，Text box internal display`description`，`default_value`For the default value;
        The second parameter，Name`advanced_arg`，Parameters`type`Declare this as a text box，Displayed above the text box`title`，Text box internal display`description`，`default_value`For the default value;
        The third parameter，Name`allow_cache`，Parameters`type`Declare that this is a dropdown menu，Display above the dropdown menu`title`+`description`，The options in the dropdown menu are`options`，`default_value`As the default value for the dropdown menu;

        """
        gui_definition = {
            "main_input":
                ArgProperty(title="ArxivID", description="Enter the Arxiv ID or URL", default_value="", type="string").model_dump_json(), # Primary input，Automatically sync from the input box
            "advanced_arg":
                ArgProperty(title="Additional translation prompts",
                            description=r"If necessary, Please provide custom translation command here, Resolve the issue of inaccurate translation for some terms。 "
                                        r"For example当单词'agent'Translation不准确When, Please try copying the following instructions to the advanced parameters section: "
                                        r'If the term "agent" is used in this section, it should be translated to "Intelligent agent". ',
                            default_value="", type="string").model_dump_json(), # Advanced parameter input area，automatic synchronization
            "allow_cache":
                ArgProperty(title="Whether to allow fetching results from the cache", options=["Allow caching", "Execute from the beginning"], default_value="Allow caching", description="None", type="dropdown").model_dump_json(),
        }
        return gui_definition

    def execute(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
        """
        Execute the plugin
        """
        allow_cache = plugin_kwargs["allow_cache"]
        advanced_arg = plugin_kwargs["advanced_arg"]

        if allow_cache == "Execute from the beginning": plugin_kwargs["advanced_arg"] = "--no-cache " + plugin_kwargs["advanced_arg"]
        yield from TranslateChineseToEnglishInLatexAndRecompilePDF(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request)



class PDF_Localize(GptAcademicPluginTemplate):
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
            "advanced_arg":
                ArgProperty(title="Additional translation prompts",
                            description=r"If necessary, Please provide custom translation command here, Resolve the issue of inaccurate translation for some terms。 "
                                        r"For example当单词'agent'Translation不准确When, Please try copying the following instructions to the advanced parameters section: "
                                        r'If the term "agent" is used in this section, it should be translated to "Intelligent agent". ',
                            default_value="", type="string").model_dump_json(), # Advanced parameter input area，automatic synchronization
            "method":
                ArgProperty(title="Which method to use for transformation", options=["MATHPIX", "DOC2X"], default_value="DOC2X", description="None", type="dropdown").model_dump_json(),

        }
        return gui_definition

    def execute(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request):
        """
        Execute the plugin
        """
        yield from TranslatePDFToChineseAndRecompilePDF(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, user_request)