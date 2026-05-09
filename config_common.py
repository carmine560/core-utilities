"""Shared configuration helpers, constants, and completion support."""

import os
import sys

try:
    from prompt_toolkit.completion import Completer, Completion

    PROMPT_TOOLKIT_IMPORT_ERROR = None
except ModuleNotFoundError as e:
    PROMPT_TOOLKIT_IMPORT_ERROR = e
    Completer = object
    Completion = None

ANSI_BOLD = "\033[1m"
ANSI_CURRENT = "\033[32m"
ANSI_ERROR = "\033[31m"
ANSI_IDENTIFIER = "\033[36m"
ANSI_RESET = "\033[m"
ANSI_UNDERLINE = "\033[4m"
ANSI_WARNING = "\033[33m"
INDENT = "    "

if sys.platform == "win32":
    os.system("color")


class ConfigError(Exception):
    """Represent a custom exception for configuration-related issues."""

    pass


class CustomWordCompleter(Completer):
    """Provide custom word completion by extending the Completer class."""

    def __init__(self, words, ignore_case=False):
        """Initialize with words for auto-completion."""
        if PROMPT_TOOLKIT_IMPORT_ERROR:
            raise ConfigError(str(PROMPT_TOOLKIT_IMPORT_ERROR))
        self.words = words
        self.ignore_case = ignore_case

    def get_completions(self, document, complete_event):
        """Yield completions for the current word before the cursor."""
        word_before_cursor = document.current_line_before_cursor.lstrip()
        for word in self.words:
            if self.ignore_case:
                if word.lower().startswith(word_before_cursor.lower()):
                    yield Completion(word, -len(word_before_cursor))
            else:
                if word.startswith(word_before_cursor):
                    yield Completion(word, -len(word_before_cursor))
