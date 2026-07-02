from __future__ import annotations

from pathlib import Path
from typing import Any

from src.graph.subgraphs.rag_subgraph import build_rag_subgraph
from src.graph.supervisor_graph import build_supervisor_graph
from src.ingestion.indexer import KnowledgeBaseIndexer
from src.ingestion.loaders import load_file_as_documents, load_pasted_text_as_documents
from src.tools.retrievers.doc_retriever import DocumentRetriever


class CybersecurityCopilotService:
    """
    Central service layer for the whole application.

    Responsibilities:
    - own the vector store
    - own the retriever
    - build the RAG subgraph
    - build the supervisor graph
    - expose simple methods for ingestion and analysis

    The UI will call this service instead of talking to the graph directly.
    """

    def __init__(self):
        self.indexer = KnowledgeBaseIndexer()
        self.vectorstore = self.indexer.get_vectorstore()
        self.retriever = DocumentRetriever(self.vectorstore)
        self.rag_graph = build_rag_subgraph(self.retriever)
        self.graph = build_supervisor_graph(self.rag_graph)

    def ingest_file(self, file_path: str | Path) -> None:
        documents = load_file_as_documents(file_path)
        self.vectorstore = self.indexer.add_documents(documents)
        self.retriever = DocumentRetriever(self.vectorstore)
        self.rag_graph = build_rag_subgraph(self.retriever)
        self.graph = build_supervisor_graph(self.rag_graph)

    def ingest_text(self, text: str, source_name: str = "pasted_text") -> None:
        documents = load_pasted_text_as_documents(text, source_name=source_name)
        self.vectorstore = self.indexer.add_documents(documents)
        self.retriever = DocumentRetriever(self.vectorstore)
        self.rag_graph = build_rag_subgraph(self.retriever)
        self.graph = build_supervisor_graph(self.rag_graph)

    def analyze(self, user_text: str, uploaded_text: str = "") -> dict[str, Any]:
        """
        Run the supervisor graph and return the final state dictionary.
        """
        state = {
            "user_text": user_text,
            "uploaded_text": uploaded_text,
        }
        return self.graph.invoke(state)
        return result