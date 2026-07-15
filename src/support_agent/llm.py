"""Factories for the chat model (used inside the graph) and the judge model (used only bu eval/)."""

from langhain_openai import ChatOpenAI
from support_agent import config

def get_chat_model(temperature: float = 0.0) -> ChatOpenAI:
    return ChatOpenAI(model=config.CHAT_MODEL_NAME, api_key=config.OPENAI_API_KEY)

def get_judge_model() -> ChatOpenAI:
    return ChatOpenAI(model=config.JUDE_MODEL_NAME, api_key=config.OPENAI_API_KEY)
