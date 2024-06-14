from contextvars import ContextVar
from intelliw.utils.intelliwapi.request import Request

_request_scope_context_storage: ContextVar[str] = ContextVar(
    "ctx", default=None
)
