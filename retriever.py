from database import collection
from config import TOP_K


def retrieve(question, k=TOP_K):

    results = collection.query(
        query_texts=[question],
        n_results=k,
    )

    retrieved_docs = []

    if not results["documents"]:
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