import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from config import COLLECTION_NAME, DB_PATH, EMBEDDING_MODEL

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
        _client = chromadb.PersistentClient(path=DB_PATH)

    return _client


def get_collection():
    global _collection

    if _collection is None:
        _collection = get_client().get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=get_embedding_function(),
        )

    return _collection
