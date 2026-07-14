"""Escalation worker: deterministic hand-off, no LLM call needed.

This is the supervisor's direct routing target for "the customer explicitly
asked for a human." The escalate_to_human tool (tools/escalation_tools.py)
is a separate path: it lets *workers* trigger escalation mid-conversation
when they judge it necessary. Both paths converge on escalated=True.
"""

from typing import Literal

from langchain_core.messages import AIMessage
from langgraph.types import Command

from support_agent.state import SupportState

def escalation_node(state: SupportState) -> Command[Literal["supervisor"]]:
    message = AIMessage(
        content="I'm connecting you with a human agent who can help further. "
    )
    return Command(goto="supervisor", update={"escalated":True, "messgaes":[message]})