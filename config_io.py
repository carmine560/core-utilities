"""Configuration file I/O with optional GPG encryption support."""

import os
from io import StringIO

from .config_common import ConfigError
from .errors import UtilityOperationError
from .file_utilities import (
    read_encrypted_file,
    write_encrypted_file,
    write_file_atomically,
)


def _config_read_error(error):
    """Add config-specific wording to low-level encrypted file errors."""
    message = str(error)
    if message.startswith("GPG decryption timed out after "):
        return message.replace(
            "GPG decryption timed out after ",
            "GPG decryption timed out while reading config after ",
            1,
        )
    if message.startswith("GPG decryption failed: "):
        return message.replace(
            "GPG decryption failed: ",
            "GPG decryption failed while reading config: ",
            1,
        )
    if message == "GPG decryption returned no file data.":
        return "GPG decryption returned no config data."
    return message


def _config_write_error(error):
    """Add config-specific wording to low-level encrypted file errors."""
    message = str(error)
    if message == "GPG encryption returned no file data.":
        return "GPG encryption returned no config data."
    return message


def read_config(config, config_path, is_encrypted=False):
    """Read config from a file, decrypt if is_encrypted is True."""
    if is_encrypted:
        encrypted_config_path = f"{config_path}.gpg"
        if os.path.isfile(encrypted_config_path):
            try:
                decrypted_data = read_encrypted_file(encrypted_config_path)
            except UtilityOperationError as e:
                raise ConfigError(_config_read_error(e)) from e
            config.read_string(decrypted_data.decode("utf-8"))
    else:
        config.read(config_path, encoding="utf-8")


def write_config(config, config_path, is_encrypted=False):
    """Write config to a file, encrypt if is_encrypted is True."""
    if is_encrypted:
        fingerprint = config.get("General", "fingerprint", fallback="")
        config_string = StringIO()
        config.write(config_string)
        try:
            write_encrypted_file(
                f"{config_path}.gpg",
                config_string.getvalue().encode("utf-8"),
                fingerprint=fingerprint,
            )
        except UtilityOperationError as e:
            raise ConfigError(_config_write_error(e)) from e
    else:
        write_file_atomically(config_path, "w", lambda f: config.write(f))
