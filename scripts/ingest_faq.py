"""Builds a local Chroma vector store from data/faq_docs/*.md.

Re-run this whenever the FAQ docs change. It deletes any existing
collection first so re-running doesn't duplicate chunks.
"""

from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

from support_agent import config

REPO_ROOT = Path(__file__).resolve().parent.parent
FAQ_DIR = REPO_ROOT / "data" / "faq_docs"

def main() -> None:
    loader = DirectoryLoader(str(FAQ_DIR), glob="*.md", loader_cls=TextLoader)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name = config.EMBEDDING_MODEL_NAME)

    existing = Chroma(persist_directory=config.CHROMA_PERSIST_DIR, embedding_function=embeddings)
    existing.delete_collection()

    Chroma.from_documents(chunks, embeddings, persist_directory=config.CHROMA_PERSIST_DIR)

    print(f"Ingested {len(docs)} source files -> {len(chunks)} chunks")
    print(f"Persisted to: {config.CHROMA_PERSIST_DIR}")

if __name__ == "__main__":
    main()

