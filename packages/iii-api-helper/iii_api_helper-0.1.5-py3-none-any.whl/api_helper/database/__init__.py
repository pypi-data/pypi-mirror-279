try:
    import sqlmodel

except ImportError:
    error_message: str = "SQLModel is not installed. Run `pip install iii-api-helper[database]`"
    raise ImportError(error_message) from None

from .pagination import common_query
from .pagination import paginate
