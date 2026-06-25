import chromadb
from pathlib import Path

from config import DB_PATH, COLLECTION_NAME, DATA_FILE


def load_text_file(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")


def chunk_text(text: str) -> list[str]:
    chunks = [chunk.strip() for chunk in text.splitlines() if chunk.strip()]
    return chunks


def ingest_documents():
    text = load_text_file(DATA_FILE)
    chunks = chunk_text(text)

    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    metadatas = [
        {
            "source": DATA_FILE,
            "chunk": i
        }
        for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas
    )

    print("Documents ingested successfully.")
    print(f"Total chunks stored: {len(chunks)}")


if __name__ == "__main__":
    ingest_documents()