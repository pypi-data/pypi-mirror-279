from logging import Logger
from logging import getLogger
from typing import TYPE_CHECKING

from fastapi import Query
from sqlalchemy import func

from ..errors import PaginationError
from ..types import PaginateQuery
from ..types import Pagination

if TYPE_CHECKING:
    from collections.abc import Sequence

try:
    from sqlmodel import Session
    from sqlmodel.sql.expression import Select
    from sqlmodel.sql.expression import SelectOfScalar

except ImportError:
    _msg: str = "SQLModel is not installed. Run `pip install iii-api-helper[database]`"
    raise ImportError(_msg) from None

logger: Logger = getLogger(__name__)


def _get_count(*, session: Session, query: Select | SelectOfScalar) -> int:
    # https://github.com/tiangolo/sqlmodel/issues/494#issuecomment-2008063162
    for count in session.exec(query.with_only_columns(func.count()).order_by(None).select_from(*query.froms)):
        return count
    return 0


def _validate_params(*, page: int, per_page: int) -> None:
    error_message: str = ""

    if page < 1:
        error_message = "Page must be greater than 0"

    if per_page < 1:
        error_message = "Per page must be greater than 0"

    if error_message:
        raise PaginationError(error_message)


def common_query(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=100, ge=1),
) -> PaginateQuery:
    return PaginateQuery(page=page, per_page=per_page)


def paginate(
    *,
    session: Session,
    query: Select | SelectOfScalar,
    page: int = 1,
    per_page: int = 10,
) -> Pagination:
    _validate_params(page=page, per_page=per_page)

    items: Sequence = session.exec(query.offset((page - 1) * per_page).limit(per_page)).all()
    total: int = _get_count(session=session, query=query)
    pages: int = max(1, (total - 1) // per_page + 1)

    if page > pages:
        raise PaginationError()

    return {
        "items": items,
        "pagination": {
            "total": total,
            "page": page,
            "pages": pages,
            "per_page": per_page,
            "prev": page - 1 if page > 1 else None,
            "next": page + 1 if page < pages else None,
        },
    }
