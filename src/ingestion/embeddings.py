from langchain_huggingface import HuggingFaceEmbeddings


def build_embeddings():
    """
    Build embedding model for the vector database.

    Using HuggingFace embeddings avoids dependency on
    Google's embedding APIs and works completely locally.
    """

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )