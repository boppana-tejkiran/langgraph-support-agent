"""Shared pytest fixtures.

Sets dummy required env vars before any support_agent import so
config.py's `os.environ[...]` reads dont blow up in CI\local runs
without a real .env file. Tests that need a live OpenAI call are
expected to be run manually with a real key set.
"""

import os

os.environ.setdefault("OPEN_API_KEY", "sk-test-dummy")
os.environ.setdefault("POSTGRES_URL", "postgresql://support_agent:support_agent@localhost:5432/support_agent")

import pytest
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

from support_agent.graph import build_graph

requires_real_openai_key = pytest.mark.skipif(
    os.environ["OPENAI_API_KEY"] == "sk-test-dummy",
    reason="requires a real OPENAI_API_KEY to call the LLM",
)

@pytest.fixture()
def test_graph():
    return build_graph(checkpointer=InMemorySaver(), store=InMemorySaver())