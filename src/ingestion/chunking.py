from __future__ import annotations

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
    documents: List[Document],
    chunk_size: int = 1200,
    chunk_overlap: int = 150,
) -> List[Document]:
    """
    Split documents into manageable chunks for embedding and retrieval.

    LangChain recommends RecursiveCharacterTextSplitter for generic text
    because it tries to preserve paragraphs, then sentences, then words
    as long as possible.
    """
    if not documents:
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    return splitter.split_documents(documents)