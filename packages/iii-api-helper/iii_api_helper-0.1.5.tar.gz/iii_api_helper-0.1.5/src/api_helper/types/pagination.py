from collections.abc import Sequence
from typing import Generic
from typing import TypeVar

from pydantic import BaseModel
from typing_extensions import TypedDict

T = TypeVar("T")


class PaginateQuery(BaseModel):
    page: int
    per_page: int


class Paginate(TypedDict):
    total: int
    page: int
    pages: int
    per_page: int
    prev: int | None
    next: int | None


class Pagination(TypedDict, Generic[T]):
    items: Sequence[T]
    pagination: Paginate
