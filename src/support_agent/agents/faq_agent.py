"""FAQ/RAG worker: answers policy/how-to questions using only retrieved FAQ content."""

from typing import Literal

from langgraph.prebuilt import create_react_agent
from langgraph.types import Command

from support_agent.llm import get_chat_model
from support_agent.state import SupportState
from support_agent.tools.faq_tools import search_faq

SYSTEM_PROMPT = """You are the FAQ specialist on a customer support team. Answer only using \
information returned by the search_faq tool. If the tool doesn't return anything relevant, \
say so plainly rather than guessing or inventing policy details.

{memory_context}
"""

def _prompt(state: SupportState) -> list:
    from langchain_core.messages import SystemMessage

    return [SystemMessage(SYSTEM_PROMPT.format(memory_context=state.get("memory_context", "")))] + state["messages"]

_agent = create_react_agent(
    model=get_chat_model(temperature=0.2),
    tools=[search_faq],
    state_schema=SupportState,
    prompt=_prompt,
)

def faq_node(state: SupportState) -> Command[Literal["supervisor"]]:
    result = _agent.invoke(state)
    return Command(goto="supervisor", update={"messages": result["messages"]})