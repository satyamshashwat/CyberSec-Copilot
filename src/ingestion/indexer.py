from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document

from src.core.settings import settings
from src.ingestion.chunking import split_documents
from src.ingestion.embeddings import build_embeddings


class KnowledgeBaseIndexer:
    """
    Builds and maintains the vector store for uploaded documents.

    Workflow:
    1. Load documents
    2. Chunk them
    3. Embed them
    4. Store them in Chroma
    5. Let retrievers query them later
    """

    def __init__(self, persist_directory: str | Path | None = None):
        self.persist_directory = Path(
            persist_directory or (settings.vectorstore_dir / "cyber_kb")
        )
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.embeddings = build_embeddings()
        self.vectorstore = Chroma(
            collection_name="cyber_kb",
            embedding_function=self.embeddings,
            persist_directory=str(self.persist_directory),
        )

    def add_documents(self, documents: List[Document]) -> Chroma:
        """
        Add new documents to the persistent knowledge base.
        """
        if not documents:
            return self.vectorstore

        chunks = split_documents(documents)
        if chunks:
            self.vectorstore.add_documents(chunks)

        return self.vectorstore

    def get_vectorstore(self) -> Chroma:
        """
        Return the current vector store instance.
        """
        return self.vectorstore