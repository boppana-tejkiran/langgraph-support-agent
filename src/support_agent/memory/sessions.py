"""Session registry: let us answer "which thread_ids belong to this customer_id?"

The checkpointer only supports loading history for a single known
thread_id; it can't enumerate threads for a customer. Long-term store
namespace (customer_id, "sessions") fills that gap. 
"""
from datetime import datetime, timezone
from langgraph.store.base import BaseStore

def register_session(store: BaseStore, customer_id: str, thread_id: str) -> None:
    store.put((customer_id, "sessions"), thread_id, {"started_at": datetime.now(timezone.utc).isoformat()})

def list_sessions(store: BaseStore, customer_id: str) -> list[str]:
    return [item.key for item in store.search((customer_id, "sessions"))]