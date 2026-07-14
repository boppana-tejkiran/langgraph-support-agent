"""Ticketing worker: files support tickets and processes refunds."""

from typing import Literal

from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from langgraph.types import Command

from support_agent.llm import get_chat_model
from support_agent.state import SupportState
from support_agent.tools.ticketing_tools import create_ticket, process_refund

SYSTEM_PROMPT= """You are the ticketing specialist on a customer support team. Before taking \
a destructive action(processing a refund or filing a ticket), confirm the order/customer \
details you found and summarize the result clearly fro the customer afterward.

{memory_context}
"""

def _prompt(state: SupportState) -> list:
    return [SystemMessage(SYSTEM_PROMPT.format(memory_context=state.get("memory_context", "")))] + state["messages"]

_agent = create_react_agent(
    model=get_chat_model(temperature=0.2),
    tools=[create_ticket, process_refund],
    state_schema=SupportState,
    prompt=_prompt
)

def ticketing_node(state: SupportState) -> Command([Literal["supervisor"]]):
    result = _agent.invoke(state)
    return Command(goto="supervisor", update={"messages":result["messages"]})