from datetime import datetime
from typing import Generic
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class SuccessModel(BaseModel, Generic[T]):
    data: T
    datetime: datetime


class ErrorModel(BaseModel, Generic[T]):
    error: T
    datetime: datetime
