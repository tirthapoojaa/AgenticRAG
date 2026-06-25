import chromadb

from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction,
)

from config import (
    DB_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
)

print("Loading embedding model...")

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)

print("Embedding model loaded.")

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function,
)