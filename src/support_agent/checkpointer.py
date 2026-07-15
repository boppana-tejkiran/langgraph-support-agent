"""Short-term (per-thread) checkpointer, backed by Postgres.

Cached as a module-level singleton for the same reason as the store:
PostgresSaver owns a connection pool that should be reused.
"""
from langgraph.checkpoint.postgres import PostgresSaver
from support_agent import config

_checkpointer: PostgresSaver | None = None
_checkpointer_cm = None

def get_checkpointer() -> PostgresSaver:
    global _checkpointer, _checkpointer_cm
    if _checkpointer is None:
        _checkpointer_cm = PostgresSaver.from_conn_string(config.POSTGRES_URL)
        _checkpointer = _checkpointer_cm.__enter__()
        _checkpointer.setup()
    return _checkpointer