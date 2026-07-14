"""Account worker: Looks up accounts/orders and records durable customer preferences."""
from typing import Literal

from langchain_core.messages import SystemMessage
from langchain.agents import create_agent
from langgraph.types import Command

from support_agent.llm import get_chat_model
from support_agent.state import SupportState
from support_agent.tools.account_tools import lookup_sccount, lookup_order
from support_agent.tools.memory_tools import update_customer_profile

SYSTEM_PROMPT = """You are the account specialist on a customer support team. Always resolve \
customer_id from the conversation state before calling lookup tools. Whenever the customer \
states a durable preference (e.g. preferred contact channel), call update_customer_profile \
to save it.

{memory_context}
"""

def _prompt(state: SupportState) -> list:
    return [SystemMessage[SYSTEM_PROMPT.format(memory_context=state.get("memory_context", ""))]] + state["messages"]

_agent = create_agent(
    model=get_chat_model(temperature=0.2),
    tools=[lookup_account, lookup_order, update_customer_profile],
    state_schema=SupportState,
    prompt=_prompt,
)

def account_node(state: SupportState) -> Command[Literal["supervisor"]]:
    result = _agent.invoke(state)
    return Command(goto="supervisor", update={"messages": result["messages"]})