from typing import Annotated

from langchain_core.tools import tool
from  langgraph.prebuilt import InjectedStore
from langgraph.store.base import BaseStore

@tool
def update_customer_profile(
    customer_id: str,
    key: str,
    value: str,
    store: Annotated[BaseStore, InjectedStore()]
) -> str:
    """Record a durable fact or preference about a customer (e.g. preferred contact channel)."""
    store.put((customer_id, "profile"), key, {"value": value})
    return f"Saved preference: {key} = {value}"