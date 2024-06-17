import uuid
from datetime import datetime
from logging import Logger
from logging import getLogger
from uuid import UUID

from sqlalchemy import UUID as SA_UUID
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import text

try:
    from sqlmodel import Field

except ImportError:
    _msg: str = "SQLModel is not installed. Run `pip install iii-api-helper[database]`"
    raise ImportError(_msg) from None

logger: Logger = getLogger(__name__)


class UUIDPrimaryKeyMixin:
    uuid: UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
        sa_type=SA_UUID,
        sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True},
    )


class TimestampMixin:
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_type=DateTime,
        sa_column_kwargs={"server_default": func.now()},
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_type=DateTime,
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )
