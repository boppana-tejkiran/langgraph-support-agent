from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.managed import RemainingSteps
from typing_extensions import TypedDict

class SupportState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    next: str
    customer_id: str | None
    escalated: bool
    memory_context: str
    remaining_steps: RemainingSteps