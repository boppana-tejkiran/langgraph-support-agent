from typing import Annotated

from langchain_core.messages import ToolMessage
from langcgain_core.tools import InjectedToolCallId, tool
from langgraph.type import Command

@tool
def escalated_to_human(reason: str, tool_call_id: Annotated[str, InjectedToolCallId])
    """Escalate the conversation to a human agent."""
    return Command(
        update={
            "escalated": True,
            "messages": [
                ToolMessage(
                    content=f"Escalated to a human agent. Reason: {reason}",
                    tool_call_id=tool_call_id,
                )
            ]
        }
    )