"""Configuration diffing and reconciliation workflow utilities."""

import configparser

from .config_common import (
    ANSI_BOLD,
    ANSI_CURRENT,
    ANSI_IDENTIFIER,
    ANSI_RESET,
    ANSI_WARNING,
)
from .config_io import read_config, write_config
from .config_prompt import tidy_answer
from . import file_utilities


def _truncate_string(string, max_length=256):
    """Truncate string to maximum length."""
    if len(string) > max_length:
        return string[:max_length] + "..."
    return string


def _collect_sections(default_config, excluded_sections):
    """Return non-empty default config sections, excluding given ones."""
    return [
        section
        for section in default_config.sections()
        if section not in excluded_sections and default_config.options(section)
    ]


def _collect_options(
    default_config, user_config, section, user_option_ignored_sections
):
    """Return default and user-only options unless section is ignored."""
    options = list(default_config.options(section))
    if section in user_option_ignored_sections:
        return options

    for option in user_config[section]:
        if option not in default_config[section]:
            options.append(option)
    return options


def _print_option_diff(
    section, option, default_value, user_value, default_config, option_indices
):
    """Print formatted diff between default and user option values."""
    if not option_indices:
        print(f"[{ANSI_BOLD}{section}{ANSI_RESET}]")

    if default_config.has_option(section, option):
        default_display = (
            _truncate_string(default_value)
            if default_value
            else f"{ANSI_WARNING}(empty){ANSI_RESET}"
        )
    else:
        default_display = f"{ANSI_WARNING}(not exist){ANSI_RESET}"

    user_display = (
        f"{ANSI_CURRENT}{_truncate_string(user_value)}{ANSI_RESET}"
        if user_value
        else f"{ANSI_WARNING}(empty){ANSI_RESET}"
    )

    print(
        f"{ANSI_IDENTIFIER}{option}{ANSI_RESET}: "
        f"{default_display} -> {user_display}"
    )


def check_config_changes(
    default_config,
    config_path,
    excluded_sections=(),
    user_option_ignored_sections=(),
    backup_parameters=None,
    is_encrypted=False,
):
    """Compare default and user configurations."""
    if backup_parameters:
        file_utilities.backup_file(config_path, **backup_parameters)

    section_index = 0
    section_indices = []
    sections = _collect_sections(default_config, excluded_sections)

    user_config = configparser.ConfigParser(interpolation=None)
    read_config(user_config, config_path, is_encrypted=is_encrypted)

    while section_index < len(sections):
        section = sections[section_index]
        answer = ""

        if not user_config.has_section(section):
            user_config.add_section(section)

        option_index = 0
        option_indices = []
        options = _collect_options(
            default_config, user_config, section, user_option_ignored_sections
        )

        while option_index < len(options):
            option = options[option_index]
            default_value = default_config[section].get(option)
            user_value = user_config[section].get(option)

            if user_value is not None and default_value != user_value:
                _print_option_diff(
                    section,
                    option,
                    default_value,
                    user_value,
                    default_config,
                    option_indices,
                )

                answers = ["default", "back", "quit"]
                if not section_indices and not option_indices:
                    answers.remove("back")

                answer = tidy_answer(answers)

                if answer == "default":
                    user_config.remove_option(section, option)
                    write_config(
                        user_config, config_path, is_encrypted=is_encrypted
                    )
                elif answer == "back":
                    if option_indices:
                        option_index = option_indices.pop()
                        continue
                    break
                elif answer == "quit":
                    return

                option_indices.append(option_index)

            option_index += 1

        if answer == "back":
            section_index = section_indices.pop()
            continue
        if option_indices:
            section_indices.append(section_index)

        section_index += 1
