from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    CSVLoader,
    PyPDFLoader,
    TextLoader,
)

TEXT_EXTENSIONS = {
    ".txt",
    ".md",
    ".log",
    ".json",
    ".yaml",
    ".yml",
}


def load_pasted_text_as_documents(
    text: str,
    source_name: str = "pasted_text",
) -> List[Document]:

    cleaned = text.strip()

    if not cleaned:
        return []

    return [
        Document(
            page_content=cleaned,
            metadata={
                "source": source_name,
                "file_name": source_name,
                "file_type": "text",
            },
        )
    ]


def load_file_as_documents(
    file_path: str | Path,
) -> List[Document]:

    path = Path(file_path)
    ext = path.suffix.lower()

    if ext == ".pdf":
        docs = PyPDFLoader(str(path)).load()

    elif ext == ".csv":
        docs = CSVLoader(
            file_path=str(path),
            encoding="utf-8",
        ).load()

    elif ext in TEXT_EXTENSIONS:
        docs = TextLoader(
            str(path),
            encoding="utf-8",
        ).load()

    else:
        raise ValueError(
            f"Unsupported file type: {ext}"
        )

    for doc in docs:
        doc.metadata.setdefault(
            "source",
            str(path),
        )

        doc.metadata.setdefault(
            "file_name",
            path.name,
        )

        doc.metadata.setdefault(
            "file_type",
            ext.lstrip("."),
        )

    return docs