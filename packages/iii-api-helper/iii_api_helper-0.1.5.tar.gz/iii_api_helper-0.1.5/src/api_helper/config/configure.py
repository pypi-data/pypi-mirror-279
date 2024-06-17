import contextlib
import logging.config
import os
from ast import literal_eval
from logging import Logger
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from ..errors import ConfigError

logger: Logger = logging.getLogger(__name__)

FALLBACK_CONFIGS: dict[str, Any] = {
    "APP_NAME": "Backend API",
    "DEBUG": False,
    "RELOAD": False,
}


def _convert_bool(value: str) -> bool:
    """Convert the string value to boolean value.

    Args:
    ----
        value: The string value

    Returns:
    -------
        bool: The boolean value

    """
    if value.lower() in ["true", "t", "1", "yes", "y", "on"]:
        return True

    elif value.lower() in ["false", "f", "0", "no", "n", "off"]:
        return False

    else:
        msg: str = f"Cannot convert {value} to boolean value."
        raise ConfigError(msg)


def _auto_convert(env: Any) -> Any:
    if isinstance(env, str):
        try:
            env = _convert_bool(env)

        except ConfigError:
            with contextlib.suppress(ValueError, SyntaxError):
                # Auto guess type, only support int, float, list, dict
                env = literal_eval(env)

    elif env is None:
        env = None

    else:
        msg: str = f"Cannot convert {env}, should be a string or None."
        raise ConfigError(msg)

    return env


def get(key: str, default: Any = None, *, convert: bool = False, raise_error: bool = False) -> Any:
    """Get the value of the key from the config file, if not found, return the default value.

    Args:
    ----
        key: The key of the config
        default: The default value if the key is not found
        convert: If the value should be converted to the correct type, otherwise, return the string type value
        raise_error: If the key is not found and the default value is None, raise the KeyError

    Returns:
    -------
        Any: The value of the key

    """
    logger.debug("Get config key %s", key)
    env: Any = os.getenv(key)

    if convert:
        env = _auto_convert(env)

    if env is not None:
        return env

    if key in FALLBACK_CONFIGS and FALLBACK_CONFIGS[key] is not None:
        return FALLBACK_CONFIGS[key]

    else:
        if raise_error and default is None:
            msg: str = f"Key '{key}' not found."
            raise ConfigError(msg)

        return default


def load_config(env_file: Path) -> None:
    logger.debug("Load env file from %s", env_file)

    if env_file.is_file() and env_file.exists():
        load_dotenv(dotenv_path=env_file, override=True)

    elif env_file.is_dir() and (dot_env := env_file / ".env").exists():
        load_dotenv(dotenv_path=dot_env, override=True)

    else:
        msg: str = f"The env file {env_file} does not exist or is not a directory containing .env file."
        raise ConfigError(msg)
