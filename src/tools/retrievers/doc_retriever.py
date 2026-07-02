from __future__ import annotations

from typing import Any, List

from langchain_chroma import Chroma
from langchain_core.documents import Document


class DocumentRetriever:
    """
    Thin wrapper around the vector store retriever.

    We keep this separate because later we may swap:
    - top-k policy
    - reranking
    - hybrid retrieval
    - filters by file type or source
    """

    def __init__(self, vectorstore: Chroma, default_k: int = 4):
        self.vectorstore = vectorstore
        self.default_k = default_k

    def retrieve(self, query: str, k: int | None = None) -> List[Document]:
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": k or self.default_k}
        )
        return retriever.invoke(query)

    @staticmethod
    def serialize_documents(documents: List[Document]) -> List[dict[str, Any]]:
        """
        Convert Documents into plain dictionaries so graph state remains serializable.
        """
        output: List[dict[str, Any]] = []

        for doc in documents:
            output.append(
                {
                    "page_content": doc.page_content,
                    "metadata": doc.metadata or {},
                }
            )

        return output

    @staticmethod
    def format_documents_for_context(documents: List[Document]) -> str:
        """
        Turn retrieved docs into a readable context block for the RAG prompt.
        """
        if not documents:
            return "No supporting documents were retrieved."

        blocks: list[str] = []
        for idx, doc in enumerate(documents, start=1):
            meta = doc.metadata or {}
            source = meta.get("file_name") or meta.get("source") or "unknown"
            page = meta.get("page")
            page_text = f", page {page}" if page is not None else ""

            blocks.append(
                f"[{idx}] Source: {source}{page_text}\n{doc.page_content}"
            )

        return "\n\n".join(blocks)