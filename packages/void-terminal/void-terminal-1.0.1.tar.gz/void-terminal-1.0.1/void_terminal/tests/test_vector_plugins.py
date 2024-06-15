"""
Test each plugin in the project。Running method：Run python tests/test_plugins.py directly
"""


import os, sys


def validate_path():
    dir_name = os.path.dirname(__file__)
    root_dir_assume = os.path.abspath(dir_name + "/..")
    os.chdir(root_dir_assume)
    sys.path.append(root_dir_assume)


validate_path()  # Return project root path

if __name__ == "__main__":
    from void_terminal.tests.test_utils import plugin_test

    plugin_test(plugin="crazy_functions.UpdateKnowledgeArchive->InjectKnowledgeBaseFiles", main_input="./README.md")

    plugin_test(
        plugin="crazy_functions.UpdateKnowledgeArchive->ReadKnowledgeArchiveAnswerQuestions",
        main_input="What is the installation method？",
    )

    plugin_test(plugin="crazy_functions.UpdateKnowledgeArchive->ReadKnowledgeArchiveAnswerQuestions", main_input="Deploy to remote cloud server？")
