__version__ = "0.1.5"  # type: str

from logging import Logger
from logging import getLogger

from .application import FastAPI
from .errors.app_error import ApplicationError
from .responses import error_response
from .responses import success_response

logger: Logger = getLogger(__name__)
