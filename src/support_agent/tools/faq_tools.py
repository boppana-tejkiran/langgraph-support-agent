from langchain_chroma import Chroma
from langchain_core.tools import tool
from langchain_huggingface import HuggingFaceEmbeddings

from support_agent import config

_embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)
_vectorstore = Chroma(persist_directory=config.CHROMA_PERSIST_DIR, embedding_function=_embeddings)

@tool
def search_faq(query: str) -> str:
    """Search the FAQ knowledge base for an answer to a customer's question."""
    docs = _vectorstore.similarity_search(query, k=3)
    if not docs:
        return "No relevant FAQ entries found."
    return "\n\n".join(f"Source: {d.metadata.get('source')}\n{d.page_content}" for d in docs)