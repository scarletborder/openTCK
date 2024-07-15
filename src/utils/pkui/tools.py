from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.completion import WordCompleter, Completer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout import (
    CompletionsMenu,
    Float,
    FloatContainer,
    HSplit,
    Layout,
    ScrollablePane,
    VSplit,
)
from prompt_toolkit.widgets import Frame, Label, TextArea
from src.battle.skills import Skill_Name_To_ID


class CustomWordCompleter(Completer):
    def __init__(self, words: list, ignore_case: bool = False):
        self.word_completer = WordCompleter(words, ignore_case=ignore_case)
        self.

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor

        # 如果第一个字符是感叹号，则为聊天内容
        if "!" == text[0]:
            return

        # 否则使用WordCompleter的补全
        yield from self.word_completer.get_completions(document, complete_event)


MyCompleter = CustomWordCompleter(list(Skill_Name_To_ID.keys()), True)
