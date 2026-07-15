"""Long-term (cross-thread) memory store, backed by Postgres.

Cached as a module-level singleton becuse PostgresStore owns a 
connection pool that should be reused, not recreated per call.
"""
from langgraph.store.postgres import PostgresStore

from support_agent import config

_store: PostgresStore | None = None
_store_cm = None

def get_store() -> PostgresStore:
    global _store, _store_cm
    if _store is None:
        _store_cm = PostgresStore.from_conn_string(config.POSTGRES_URL)
        _store = _store_cm._enter__()
        _store.setup()
    return _store