import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from config import (
    EMBEDDING_MODEL,
    MEMORY_COLLECTION_NAME,
    MEMORY_DB_PATH,
    MEMORY_TOP_K,
)

_embedding_function = None
_client = None
_collection = None


def get_embedding_function():
    global _embedding_function

    if _embedding_function is None:
        _embedding_function = SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL
        )

    return _embedding_function


def get_client():
    global _client

    if _client is None:
        _client = chromadb.PersistentClient(path=MEMORY_DB_PATH)

    return _client


def get_collection():
    global _collection

    if _collection is None:
        _collection = get_client().get_or_create_collection(
            name=MEMORY_COLLECTION_NAME,
            embedding_function=get_embedding_function(),
        )

    return _collection


def reset_memory_vector_db() -> None:
    collection = get_collection()
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])


def add_fact_to_vector_db(fact_id: str, fact_text: str, metadata: dict) -> None:
    get_collection().upsert(
        ids=[fact_id],
        documents=[fact_text],
        metadatas=[metadata],
    )


def delete_fact_from_vector_db(fact_id: str) -> None:
    get_collection().delete(ids=[fact_id])


def rebuild_memory_vector_db(facts: list[dict]) -> None:
    reset_memory_vector_db()

    for fact in facts:
        add_fact_to_vector_db(
            fact_id=fact["id"],
            fact_text=fact["fact"],
            metadata={
                "id": fact["id"],
                "category": fact.get("category", "general"),
                "confidence": fact.get("confidence", 1.0),
            },
        )


def search_memory(query: str, k: int = MEMORY_TOP_K) -> list[dict]:
    results = get_collection().query(
        query_texts=[query],
        n_results=k,
    )

    memories = []

    if not results["documents"] or not results["documents"][0]:
        return memories

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        memories.append(
            {
                "fact": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return memories
