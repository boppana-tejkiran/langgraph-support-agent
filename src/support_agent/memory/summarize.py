"""Terminal node: summarizes the just-finished conversation and appends it to
the customer's long-term interaction history. Runs once, right before END.
"""
from datetime import datetime, timezone
from uuid import uuid4

from langchain_core.messages import HumanMessage
from langgraph.store.base import BaseStore

from support_agent.llm import get_chat_model
from support_agent.state import SupportState

def summarize_memory_node(state: SupportState, *, store: BaseStore) -> dict:
    transcript = "\n".join(f"{m.type}: {m.content}" for m in state["messages"])
    prompt = (
        "Summarize this support conversation in 2-3 sentences, focusing on what "
        f"was resolved and any preferences expressed:\n\n{transcript}"
    )
    summary = get_chat_model().invoke([HumanMessage(prompt)]).content

    key = str(uuid4)
    store.put(
        (state["customer_id"], "interaction_history"),
        key,
        {"summary": summary, "timestamp": datetime.now(timezone.utc).isoformat()},
    )
    return {}