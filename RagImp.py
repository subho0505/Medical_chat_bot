from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

def query_from_text(query: str, db_path: str = "./db", k: int = 3) -> list[str]:
    """
    Query a local Chroma vector DB using HuggingFace embeddings.

    Args:
        query (str): The input query string.
        db_path (str): Path to the persisted Chroma DB directory.
        k (int): Number of top results to return.

    Returns:
        list[str]: List of matching chunk texts.
    """
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma(persist_directory=db_path, embedding_function=embeddings)
    results = vectordb.similarity_search(query, k=k)

    return [res.page_content for res in results]
