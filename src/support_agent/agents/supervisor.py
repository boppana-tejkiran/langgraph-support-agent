"""Routing node: uses structured output to pick which worker handles the next turn."""

from typing import Literal

from langchain_core.messages import SystemMessage
from langgraph.types import Command
from pydantic import BaseModel

from support_agent.llm import get_chat_model
from support_agent.state import SupportState

Destination = Literal["faq", "account", "ticketing", "escalation", "FINISH"]

class Router(BaseModel):
    next: Destination
    reasoing: str

SYSTEM_PROMPT= """You are the supervisor for a customer support system. Based on the \
conversation so far, decide whoch specialist should handle the next turn:

- faq: general policy/how-to questions (shipping, returns, billing, account how-tos)
- account: looking up account/order details, or recording a customer preference
- ticketing: filling support tickets or processing refunds
- escalation: the customer explicitly asks for a human, or is clearly frustrated/angry
- FINISH: the customer's request(s) have been fully resolved and no further action is needed.

{escalation_note}

{memory_context}
"""

def supervisor_node(state: SupportState) -> Command[Literal["faq", "account", "ticketing", "escalation", "summarize_memory"]]:
    escalation_note = (
        "The conversation has already been escalated to a human agent. Prefer FINISH unless "
        "the customer raises a new, separate request."
        if state.get("escalated")
        else ""
    )
    prompt = SYSTEM_PROMPT.format(
        escalation_note=escalation_note,
        memory_context=state.get("memory_context", "")
    )

    decision = (
        get_chat_model()
        .with_structured_output(Router)
        .invoke([SystemMessage(prompt) + state["messages"]])
    )

    if decision.next == "FINISH":
        return Command(goto="summarize_memory", update={"next": "FINISH"})
    
    return Command(goto=decision.next, update={"next":decision.next})