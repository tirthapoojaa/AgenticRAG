import hashlib
from pathlib import Path
from datetime import datetime

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from database import collection

from config import (
    DB_PATH,
    COLLECTION_NAME,
    DOCS_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
)


def load_txt_or_md(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")


def load_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    text = ""

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text:
            text += f"\n\n[Page {page_number}]\n{page_text}"

    return text


def load_document(file_path: Path) -> str:
    extension = file_path.suffix.lower()

    if extension in [".txt", ".md"]:
        return load_txt_or_md(file_path)

    if extension == ".pdf":
        return load_pdf(file_path)

    raise ValueError(f"Unsupported file type: {extension}")


def get_file_hash(file_path: Path) -> str:
    file_bytes = file_path.read_bytes()
    return hashlib.md5(file_bytes).hexdigest()


def get_supported_files() -> list[Path]:
    docs_dir = Path(DOCS_PATH)

    if not docs_dir.exists():
        raise FileNotFoundError(
            f"Folder '{DOCS_PATH}' does not exist. Create it and add your documents."
        )

    supported_extensions = {".txt", ".md", ".pdf"}

    files = [
        file
        for file in docs_dir.rglob("*")
        if file.is_file() and file.suffix.lower() in supported_extensions
    ]

    if not files:
        raise FileNotFoundError(
            f"No supported documents found in '{DOCS_PATH}'. Add .txt, .md, or .pdf files."
        )

    return files


def chunk_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    return splitter.split_text(text)


def create_collection():
    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )

    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
    )

    return collection


def clear_collection(collection):
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])


def ingest_documents():
    collection = create_collection()

    clear_collection(collection)

    files = get_supported_files()

    all_ids = []
    all_documents = []
    all_metadatas = []

    for file_path in files:
        print(f"Processing: {file_path}")

        text = load_document(file_path)
        file_hash = get_file_hash(file_path)
        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):
            chunk_id = f"{file_path.stem}_{file_hash[:8]}_{index}"

            metadata = {
                "filename": file_path.name,
                "source": str(file_path),
                "extension": file_path.suffix.lower(),
                "chunk": index,
                "file_hash": file_hash,
                "created_at": datetime.now().isoformat(),
            }

            all_ids.append(chunk_id)
            all_documents.append(chunk)
            all_metadatas.append(metadata)

    collection.add(
        ids=all_ids,
        documents=all_documents,
        metadatas=all_metadatas,
    )

    print("\nIngestion completed.")
    print(f"Files processed: {len(files)}")
    print(f"Chunks stored: {len(all_documents)}")


if __name__ == "__main__":
    ingest_documents()