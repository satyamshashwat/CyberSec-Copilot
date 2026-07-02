from __future__ import annotations

from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START, StateGraph

from src.core.llm import build_chat_model
from src.core.schemas import CybersecurityAnswer
from src.core.state import AppState
from src.graph.router import classify_route
from src.prompts.rag import RAG_SYSTEM_PROMPT
from src.tools.retrievers.doc_retriever import DocumentRetriever


def _serialize_answer(answer: Any) -> dict[str, Any]:
    """
    Convert the structured model output into a plain dictionary for graph state.
    """
    if hasattr(answer, "model_dump"):
        return answer.model_dump()
    if isinstance(answer, dict):
        return answer
    return {"raw_text": str(answer)}


def build_rag_subgraph(retriever: DocumentRetriever):
    """
    Build the specialist RAG subgraph.

    Node flow:
    1. retrieve_context
    2. generate_answer
    3. END

    This subgraph is later embedded inside the supervisor graph.
    """
    llm = build_chat_model(temperature=0.2)
    structured_llm = llm.with_structured_output(CybersecurityAnswer)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", RAG_SYSTEM_PROMPT),
            (
                "human",
                "User question:\n{question}\n\nRetrieved context:\n{context}",
            ),
        ]
    )

    def retrieve_context(state: AppState) -> dict[str, Any]:
        question = state.get("user_text", "").strip()
        docs = retriever.retrieve(question, k=4)
        serialized_docs = retriever.serialize_documents(docs)
        return {"retrieved_docs": serialized_docs}

    def generate_answer(state: AppState) -> dict[str, Any]:
        question = state.get("user_text", "").strip()
        raw_docs = state.get("retrieved_docs", [])

        # Reconstruct lightweight document objects for readable context formatting.
        from langchain_core.documents import Document

        docs = [
            Document(
                page_content=item.get("page_content", ""),
                metadata=item.get("metadata", {}),
            )
            for item in raw_docs
        ]

        context = retriever.format_documents_for_context(docs)

        chain = prompt | structured_llm
        result = chain.invoke(
            {
                "question": question,
                "context": context,
            }
        )

        return {"final_answer": _serialize_answer(result)}

    builder = StateGraph(AppState)
    builder.add_node("retrieve_context", retrieve_context)
    builder.add_node("generate_answer", generate_answer)

    builder.add_edge(START, "retrieve_context")
    builder.add_edge("retrieve_context", "generate_answer")
    builder.add_edge("generate_answer", END)

    return builder.compile()