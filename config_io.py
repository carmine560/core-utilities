"""Configuration file I/O with optional GPG encryption support."""

from io import StringIO
import os

from .config_common import ConfigError

try:
    import gnupg

    GNUPG_IMPORT_ERROR = None
except ModuleNotFoundError as e:
    GNUPG_IMPORT_ERROR = e


def read_config(config, config_path, is_encrypted=False):
    """Read config from a file, decrypt if is_encrypted is True."""
    if is_encrypted:
        encrypted_config_path = f"{config_path}.gpg"
        if os.path.isfile(encrypted_config_path):
            if GNUPG_IMPORT_ERROR:
                raise RuntimeError(GNUPG_IMPORT_ERROR)

            with open(encrypted_config_path, "rb") as f:
                encrypted_config = f.read()

            gpg = gnupg.GPG()
            decrypted_config = gpg.decrypt(encrypted_config)
            if not getattr(
                decrypted_config,
                "ok",
                bool(getattr(decrypted_config, "data", b"")),
            ):
                status = getattr(
                    decrypted_config, "status", "decryption failed"
                )
                raise ConfigError(
                    "GPG decryption failed while reading config: "
                    f"{status or 'decryption failed'}"
                )

            decrypted_data = getattr(decrypted_config, "data", b"")
            if not decrypted_data:
                raise ConfigError("GPG decryption returned no config data.")

            config.read_string(decrypted_data.decode())
    else:
        config.read(config_path, encoding="utf-8")


def write_config(config, config_path, is_encrypted=False):
    """Write config to a file, encrypt if is_encrypted is True."""
    if is_encrypted:
        if GNUPG_IMPORT_ERROR:
            raise RuntimeError(GNUPG_IMPORT_ERROR)

        gpg = gnupg.GPG()
        gpg.encoding = "utf-8"

        fingerprint = config.get("General", "fingerprint", fallback="")
        if not fingerprint:
            keys = gpg.list_keys()
            if not keys:
                raise ConfigError("No usable GPG keys found.")
            fingerprint = keys[0].get("fingerprint")
            if not fingerprint:
                raise ConfigError("GPG key has no fingerprint.")

        config_string = StringIO()
        config.write(config_string)
        encrypted_config = gpg.encrypt(
            config_string.getvalue(), fingerprint, armor=False
        )
        if not encrypted_config.ok:
            raise ConfigError(
                f"GPG encryption failed: {encrypted_config.status}"
            )
        with open(f"{config_path}.gpg", "wb") as f:
            f.write(encrypted_config.data)
    else:
        with open(config_path, "w", encoding="utf-8") as f:
            config.write(f)
