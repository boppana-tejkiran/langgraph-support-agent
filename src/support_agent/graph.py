"""Builds and compiles the StateGraph.

Only START -> load_memory -> supervisor and summarize_memory -> END are
statc edges; every other trasition is a Command(goto=...) returned by
a node, so the other five nodes appear in an add_edge call.
"""
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import START, END, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph.base import BaseStore

from support_agent.agents.account_agent import account_node
from support_agent.agents.escalation_agent import escalation_node
from support_agent.agents.faq_agent import faq_node
from support_agent.agents.supervisor import supervisor_node
from support_agent.agents.ticketing_agent import ticketing_node
from support_agent.checkpointer import get_checkpointer
from support_agent.memory.load_memory import load_memory_node
from support_agent.store import get_store
from support_agent.memory.summarize import summarize_memory_node
from support_agent.state import SupportState

def build_graph(
        checkpointer: BaseCheckpointSaver | None = None,
        store: BaseStore | None = None,
) -> CompiledStateGraph:
    workflow = StateGraph(SupportState)
    workflow.add_node("load_memory", load_memory_node)
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("faq", faq_node)
    workflow.add_node("account", account_node)
    workflow.add_node("ticketing", ticketing_node)
    workflow.add_node("escalation", escalation_node)
    workflow.add_node("summarize_memory", summarize_memory_node)

    workflow.add_edge(START, "load_memory")
    workflow.add_edge("load_memory", "supervisor")
    workflow.add_edge("summarize_memory", END)

    return workflow.compile(
        checkpointer=checkpointer or get_checkpointer(),
        store=store or get_store(),
    )

graph = None

def get_graph() -> CompiledStateGraph:
    global graph
    if graph is None:
        graph = build_graph()
    return graph