"""Configuration parsing, structure, and validation utilities."""

import ast

from .config_common import ConfigError


def ensure_section_exists(config, section):
    """Ensure a section is defined, raise ConfigError if not."""
    if not config.has_section(section):
        raise ConfigError(f"The '{section}' section is undefined.")


def list_section(config, section):
    """Retrieve all options from a specified section in a configuration."""
    options = []
    if config.has_section(section):
        for option in config[section]:
            options.append(option)
        return options

    raise ConfigError(f"The '{section}' section does not exist.")


def get_strict_boolean(config, section, option):
    """Retrieve a strict boolean value from a configuration section."""
    value = config.get(section, option)
    if value.lower() not in {"true", "false"}:
        raise ValueError(f"Invalid boolean value for {option} in {section}.")
    return config.getboolean(section, option)


def evaluate_value(value):
    """Evaluate the given value using Python's abstract syntax trees."""
    evaluated_value = None
    try:
        evaluated_value = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        pass
    except (TypeError, MemoryError, RecursionError) as e:
        raise ConfigError(f"Unable to evaluate config value: {e}") from e
    return evaluated_value
