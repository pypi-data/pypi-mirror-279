class APIHelperBaseError(Exception):
    """Base exception for API helper."""


class ConfigError(APIHelperBaseError):
    """Base exception for config error."""


class FastAPIError(APIHelperBaseError):
    """Base exception for FastAPI related error."""
