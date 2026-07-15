"""First-turn node: registers the current thread under the customer's session
registry, then reads long-term memory (profile + recent interaction summaries)
and injects it into state as `memory_context` for the supervisor/workers to read.
"""
from langchain_core.runnables import RunnableConfig
from langgraph.store.base import BaseStore

from support_agent.memory.sessions import register_session
from support_agent.state import SupportState

def load_memory_node(state: SupportState, config: RunnableConfig, *, store: BaseStore) -> dict:
    if len(state["messages"]) > 1:
        return {}
    
    customer_id = state["customer_id"]
    thread_id = config["configurable"]["thread_id"]
    register_session(store, customer_id, thread_id)

    profile_items = store.search((customer_id, "profile"))
    history_items = store.search((customer_id, "interaction_history"), limits=3)

    profile_text = "; ".join(f"{item.key}={item.value['value']}" for item in profile_items) or "none known"
    history_text = (
        "\n".join(
            item.value["summary"]
            for item in sorted(history_items, key=lambda i:i.value["timestamp"])
        )
        or "no prior interactions"
    )

    memory_context = f"Known customer preferences: {profile_text}\nSummary of past interactions:\n{history_text}"
    return {"memory_context": memory_context}

