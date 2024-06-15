import os
from textwrap import indent

class FileNode:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.is_leaf = False
        self.level = 0
        self.parenting_ship = []
        self.comment = ""
        self.comment_maxlen_show = 50

    @staticmethod
    def add_linebreaks_at_spaces(string, interval=10):
        return '\n'.join(string[i:i+interval] for i in range(0, len(string), interval))

    def sanitize_comment(self, comment):
        if len(comment) > self.comment_maxlen_show: suf = '...'
        else: suf = ''
        comment = comment[:self.comment_maxlen_show]
        comment = comment.replace('\"', '').replace('`', '').replace('\n', '').replace('`', '').replace('$', '')
        comment = self.add_linebreaks_at_spaces(comment, 10)
        return '`' + comment + suf + '`'

    def add_file(self, file_path, file_comment):
        directory_names, file_name = os.path.split(file_path)
        current_node = self
        level = 1
        if directory_names == "":
            new_node = FileNode(file_name)
            current_node.children.append(new_node)
            new_node.is_leaf = True
            new_node.comment = self.sanitize_comment(file_comment)
            new_node.level = level
            current_node = new_node
        else:
            dnamesplit = directory_names.split(os.sep)
            for i, directory_name in enumerate(dnamesplit):
                found_child = False
                level += 1
                for child in current_node.children:
                    if child.name == directory_name:
                        current_node = child
                        found_child = True
                        break
                if not found_child:
                    new_node = FileNode(directory_name)
                    current_node.children.append(new_node)
                    new_node.level = level - 1
                    current_node = new_node
            term = FileNode(file_name)
            term.level = level
            term.comment = self.sanitize_comment(file_comment)
            term.is_leaf = True
            current_node.children.append(term)

    def print_files_recursively(self, level=0, code="R0"):
        print('    '*level + self.name + ' ' + str(self.is_leaf) + ' ' + str(self.level))
        for j, child in enumerate(self.children):
            child.print_files_recursively(level=level+1, code=code+str(j))
            self.parenting_ship.extend(child.parenting_ship)
            p1 = f"""{code}[\"🗎{self.name}\"]""" if self.is_leaf else f"""{code}[[\"📁{self.name}\"]]"""
            p2 = """ --> """
            p3 = f"""{code+str(j)}[\"🗎{child.name}\"]""" if child.is_leaf else f"""{code+str(j)}[[\"📁{child.name}\"]]"""
            edge_code = p1 + p2 + p3
            if edge_code in self.parenting_ship:
                continue
            self.parenting_ship.append(edge_code)
        if self.comment != "":
            pc1 = f"""{code}[\"🗎{self.name}\"]""" if self.is_leaf else f"""{code}[[\"📁{self.name}\"]]"""
            pc2 = f""" -.-x """
            pc3 = f"""C{code}[\"{self.comment}\"]:::Comment"""
            edge_code = pc1 + pc2 + pc3
            self.parenting_ship.append(edge_code)


MERMAID_TEMPLATE = r"""
```mermaid
flowchart LR
    %% <gpt_academic_hide_mermaid_code> A special mark，Used to hide code blocks when generating mermaid charts
    classDef Comment stroke-dasharray: 5 5
    subgraph {graph_name}
{relationship}
    end
```
"""

def build_file_tree_mermaid_diagram(file_manifest, file_comments, graph_name):
    # Create the root node
    file_tree_struct = FileNode("root")
    # Build the tree structure
    for file_path, file_comment in zip(file_manifest, file_comments):
        file_tree_struct.add_file(file_path, file_comment)
    file_tree_struct.print_files_recursively()
    cc = "\n".join(file_tree_struct.parenting_ship)
    ccc = indent(cc, prefix=" "*8)
    return MERMAID_TEMPLATE.format(graph_name=graph_name, relationship=ccc)

if __name__ == "__main__":
    # File manifest
    file_manifest = [
        "cradle_void_terminal.ipynb",
        "tests/test_utils.py",
        "tests/test_plugins.py",
        "tests/test_llms.py",
        "config.py",
        "build/ChatGLM-6b-onnx-u8s8/chatglm-6b-int8-onnx-merged/model_weights_0.bin",
        "crazy_functions/latex_fns/latex_actions.py",
        "crazy_functions/latex_fns/latex_toolbox.py"
    ]
    file_comments = [
        "According to position and name，May be an initialization file for a module based on position and name，May be an initialization file for a module based on position and name，May Be an Initialization File for a Module",
        "Contains functions and decorators for text processing and model fine-tuning",
        "Classes and methods for building HTML reports",
        "Contains Functions for Text Segmentation，Example code for processing PDF files includes functions for text segmentation，Example code for processing PDF files includes functions for text segmentation，And example code for handling PDF files",
        "Functions and related auxiliary functions for parsing and translating PDF files",
        "Is an initialization file for a package，The file used for initializing package properties and importing modules is an initialization file for the package，The file used for initializing package properties and importing modules is an initialization file for the package，For initializing package properties and importing modules",
        "A universal file loader for loading and splitting text in files",
        "Contains functions and classes for building and managing vector databases",
    ]
    print(build_file_tree_mermaid_diagram(file_manifest, file_comments, "Project file tree"))