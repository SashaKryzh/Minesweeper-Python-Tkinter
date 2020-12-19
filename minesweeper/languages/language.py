from types import SimpleNamespace
from minesweeper.languages.ur import ur
from minesweeper.languages.en import en

class NestedNamespace(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)

global text_messages
text_messages = {}
text_messages.update({"ur": NestedNamespace(ur)})
text_messages.update({"en": NestedNamespace(en)})