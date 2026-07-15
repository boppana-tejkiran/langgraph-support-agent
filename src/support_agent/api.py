"""FastAPI app exposing a single synchronous chat endpoint.

Streaming (graph.astream_events) is a documented follow-up, not built
into v1, to kepp the reference implementation simple.
"""
from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from support_agent.graph import get_graph

app = FastAPI(title="Support Agent API")

class ChatRequest(BaseModel):
    customer_id: str
    thread_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    escalated: bool

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    graph = get_graph()
    config = {"configurable": {"thread_id": req.thread_id}}
    result = graph.invoke(
        {"messages": [HumanMessage(req.message)], "customer_id": req.customer_id},
        config=config,
    )
    return ChatResponse(reply=result["messages"][-1].content, escalated=result.get("escalated", False))