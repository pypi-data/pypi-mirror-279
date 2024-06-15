import pickle


class SafeUnpickler(pickle.Unpickler):

    def get_safe_classes(self):
        from void_terminal.crazy_functions.latex_fns.latex_actions import LatexPaperFileGroup, LatexPaperSplit
        # Define allowed security classes
        safe_classes = {
            # Add other secure classes here
            'LatexPaperFileGroup': LatexPaperFileGroup,
            'LatexPaperSplit' : LatexPaperSplit,
        }
        return safe_classes

    def find_class(self, module, name):
        # Only allow specific classes to be deserialized
        self.safe_classes = self.get_safe_classes()
        if f'{module}.{name}' in self.safe_classes:
            return self.safe_classes[f'{module}.{name}']
        # If trying to load unauthorized class，Then throw an exception
        raise pickle.UnpicklingError(f"Attempted to deserialize unauthorized class '{name}' from module '{module}'")

def objdump(obj, file="objdump.tmp"):

    with open(file, "wb+") as f:
        pickle.dump(obj, f)
    return


def objload(file="objdump.tmp"):
    import os

    if not os.path.exists(file):
        return
    with open(file, "rb") as f:
        unpickler = SafeUnpickler(f)
        return unpickler.load()
