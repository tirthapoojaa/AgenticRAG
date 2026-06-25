import chromadb
from pathlib import Path
from datetime import datetime
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    DB_PATH,
    COLLECTION_NAME,
    DOCS_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)


def load_txt_or_md(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")


def load_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def load_document(file_path: Path) -> str:
    if file_path.suffix.lower() in [".txt", ".md"]:
        return load_txt_or_md(file_path)

    if file_path.suffix.lower() == ".pdf":
        return load_pdf(file_path)

    raise ValueError(f"Unsupported file type: {file_path.suffix}")


def chunk_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    return splitter.split_text(text)


def get_supported_files() -> list[Path]:
    docs_dir = Path(DOCS_PATH)

    supported_extensions = [".txt", ".md", ".pdf"]

    files = [
        file
        for file in docs_dir.iterdir()
        if file.is_file() and file.suffix.lower() in supported_extensions
    ]

    return files


def clear_collection(collection):
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])


def ingest_documents():
    client = chromadb.PersistentClient(path=DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    clear_collection(collection)

    files = get_supported_files()

    all_ids = []
    all_documents = []
    all_metadatas = []

    for file_path in files:
        print(f"Processing: {file_path.name}")

        text = load_document(file_path)
        chunks = chunk_text(text)

        for index, chunk in enumerate(chunks):
            chunk_id = f"{file_path.stem}_{index}"

            metadata = {
                "filename": file_path.name,
                "source": str(file_path),
                "extension": file_path.suffix,
                "chunk": index,
                "created_at": datetime.now().isoformat(),
            }

            all_ids.append(chunk_id)
            all_documents.append(chunk)
            all_metadatas.append(metadata)

    if all_documents:
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