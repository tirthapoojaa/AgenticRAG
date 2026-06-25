import chromadb

from config import DB_PATH, COLLECTION_NAME, TOP_K


def retrieve(question: str, k: int = TOP_K) -> list[dict]:
    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    results = collection.query(
        query_texts=[question],
        n_results=k,
    )

    retrieved_docs = []

    if not results["documents"]:
        return retrieved_docs

    for i in range(len(results["documents"][0])):
        retrieved_docs.append(
            {
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            }
        )

    return retrieved_docs


def print_retrieved_docs(question: str):
    docs = retrieve(question)

    print("\nRetrieved Chunks:\n")

    for i, doc in enumerate(docs, start=1):
        print(f"Result {i}")
        print(f"File: {doc['metadata']['filename']}")
        print(f"Chunk: {doc['metadata']['chunk']}")
        print(f"Distance: {doc['distance']}")
        print(doc["text"])
        print("-" * 60)


if __name__ == "__main__":
    question = input("Enter question: ")
    print_retrieved_docs(question)