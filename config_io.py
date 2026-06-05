"""Configuration file I/O with optional GPG encryption support."""

import os
import subprocess
import tempfile
from io import StringIO

from .config_common import ConfigError

GPG_TIMEOUT_SECONDS = 30


def write_file_atomically(target_path, mode, write, newline=None):
    """Write a sibling temp file before replacing the final target."""
    directory = os.path.dirname(os.path.abspath(target_path)) or "."
    prefix = f".{os.path.basename(target_path)}."
    fd, temporary_path = tempfile.mkstemp(
        prefix=prefix, suffix=".tmp", dir=directory
    )
    try:
        if "b" in mode:
            with os.fdopen(fd, mode) as f:
                write(f)
                f.flush()
                os.fsync(f.fileno())
        else:
            with os.fdopen(
                fd,
                mode,
                encoding="utf-8",
                newline=newline,
            ) as f:
                write(f)
                f.flush()
                os.fsync(f.fileno())
        os.replace(temporary_path, target_path)
        try:
            directory_fd = os.open(
                directory,
                os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
            )
        except OSError:
            directory_fd = None
        if directory_fd is not None:
            try:
                os.fsync(directory_fd)
            except OSError:
                pass
            finally:
                os.close(directory_fd)
    finally:
        if os.path.exists(temporary_path):
            os.remove(temporary_path)


def read_config(config, config_path, is_encrypted=False):
    """Read config from a file, decrypt if is_encrypted is True."""
    if is_encrypted:
        encrypted_config_path = f"{config_path}.gpg"
        if os.path.isfile(encrypted_config_path):
            try:
                decrypted_config = subprocess.run(
                    [
                        "gpg",
                        "--batch",
                        "--yes",
                        "--decrypt",
                        encrypted_config_path,
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=False,
                    timeout=GPG_TIMEOUT_SECONDS,
                )
            except subprocess.TimeoutExpired as e:
                raise ConfigError(
                    "GPG decryption timed out while reading config after "
                    f"{GPG_TIMEOUT_SECONDS} seconds."
                ) from e
            except OSError as e:
                raise ConfigError(f"Unable to run gpg: {e}") from e
            if decrypted_config.returncode:
                status = decrypted_config.stderr.decode(
                    "utf-8", errors="replace"
                ).strip()
                if not status:
                    status = (
                        "gpg exited with status "
                        f"{decrypted_config.returncode}"
                    )
                raise ConfigError(
                    f"GPG decryption failed while reading config: {status}"
                )

            decrypted_data = decrypted_config.stdout
            if not decrypted_data:
                raise ConfigError("GPG decryption returned no config data.")

            config.read_string(decrypted_data.decode("utf-8"))
    else:
        config.read(config_path, encoding="utf-8")


def write_config(config, config_path, is_encrypted=False):
    """Write config to a file, encrypt if is_encrypted is True."""
    if is_encrypted:
        fingerprint = config.get("General", "fingerprint", fallback="")
        config_string = StringIO()
        config.write(config_string)
        args = [
            "gpg",
            "--batch",
            "--yes",
            "--encrypt",
        ]
        if fingerprint:
            args.extend(["--recipient", fingerprint])
        else:
            # python-gnupg requires an explicit recipient and cannot express
            # GnuPG's default-recipient-self behavior.
            args.append("--default-recipient-self")

        try:
            encrypted_config = subprocess.run(
                args,
                input=config_string.getvalue().encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
                timeout=GPG_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired as e:
            raise ConfigError(
                "GPG encryption timed out after "
                f"{GPG_TIMEOUT_SECONDS} seconds."
            ) from e
        except OSError as e:
            raise ConfigError(f"Unable to run gpg: {e}") from e
        if encrypted_config.returncode:
            status = encrypted_config.stderr.decode(
                "utf-8", errors="replace"
            ).strip()
            if not status:
                status = (
                    f"gpg exited with status {encrypted_config.returncode}"
                )
            raise ConfigError(f"GPG encryption failed: {status}")
        if not encrypted_config.stdout:
            raise ConfigError("GPG encryption returned no config data.")
        write_file_atomically(
            f"{config_path}.gpg",
            "wb",
            lambda f: f.write(encrypted_config.stdout),
        )
    else:
        write_file_atomically(config_path, "w", lambda f: config.write(f))
