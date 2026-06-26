from config import TOP_K
from database import get_collection


def retrieve(question: str, k: int = TOP_K) -> list[dict]:
    collection = get_collection()

    results = collection.query(
        query_texts=[question],
        n_results=k,
    )

    retrieved_docs = []

    if not results["documents"] or not results["documents"][0]:
        return retrieved_docs

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        retrieved_docs.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return retrieved_docs
