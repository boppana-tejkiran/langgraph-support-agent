"""Central place for all environment/config reads."""
import os
from dotenv import load_dotenv

load_dotenv()

OPEN_API_KEY = os.environ["OPENAI_API_KEY"]
POSTGRES_URL = os.environ["POSTGRES_URL"]
CHAT_MODEL_NAME = os.getenv("CHAT_MODEL_NAME", "gpt-4o-mini")
JUDGE_MODEL_NAME = os.getenv("JUDGE_MODEL_NAME", "gpt-4o")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", ".chroma")