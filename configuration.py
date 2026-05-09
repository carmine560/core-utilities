"""Configuration management and auto-completion utilities."""

from .config_common import (
    ANSI_BOLD,
    ANSI_CURRENT,
    ANSI_ERROR,
    ANSI_IDENTIFIER,
    ANSI_RESET,
    ANSI_UNDERLINE,
    ANSI_WARNING,
    ConfigError,
    CustomWordCompleter,
    INDENT,
)
from .config_diff import check_config_changes
from .config_io import GNUPG_IMPORT_ERROR, read_config, write_config
from .config_prompt import (
    GUI_IMPORT_ERROR,
    configure_position,
    delete_option,
    modify_dictionary,
    modify_nested_value,
    modify_option,
    modify_section,
    modify_tuple,
    modify_tuple_list,
    modify_value,
    prompt_for_input,
    tidy_answer,
)
from .config_validation import (
    ensure_section_exists,
    evaluate_value,
    get_strict_boolean,
    list_section,
)

__all__ = [
    "ANSI_BOLD",
    "ANSI_CURRENT",
    "ANSI_ERROR",
    "ANSI_IDENTIFIER",
    "ANSI_RESET",
    "ANSI_UNDERLINE",
    "ANSI_WARNING",
    "ConfigError",
    "CustomWordCompleter",
    "GNUPG_IMPORT_ERROR",
    "GUI_IMPORT_ERROR",
    "INDENT",
    "check_config_changes",
    "configure_position",
    "delete_option",
    "ensure_section_exists",
    "evaluate_value",
    "get_strict_boolean",
    "list_section",
    "modify_dictionary",
    "modify_nested_value",
    "modify_option",
    "modify_section",
    "modify_tuple",
    "modify_tuple_list",
    "modify_value",
    "prompt_for_input",
    "read_config",
    "tidy_answer",
    "write_config",
]
