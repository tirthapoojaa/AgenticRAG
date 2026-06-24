import chromadb
from pathlib import Path

# ---------------------------------------------------
# Read the text file
# ---------------------------------------------------

text = Path("data.txt").read_text(encoding="utf-8")

# ---------------------------------------------------
# Split into chunks
# Each topic is separated by a blank line
# ---------------------------------------------------

chunks = [chunk.strip() for chunk in text.splitlines() if chunk.strip()]

# ---------------------------------------------------
# Create/Open Chroma database
# ---------------------------------------------------

client = chromadb.PersistentClient(path="db/chroma_db")

collection = client.get_or_create_collection(
    name="my_notes"
)

# ---------------------------------------------------
# Remove old data (optional while learning)
# ---------------------------------------------------

existing = collection.get()

if existing["ids"]:
    collection.delete(ids=existing["ids"])

# ---------------------------------------------------
# Store chunks
# ---------------------------------------------------

ids = [f"chunk_{i}" for i in range(len(chunks))]

metadatas = [
    {
        "chunk": i,
        "source": "data.txt"
    }
    for i in range(len(chunks))
]

collection.add(
    ids=ids,
    documents=chunks,
    metadatas=metadatas
)

print("=" * 60)
print("Documents stored successfully!")
print(f"Total Chunks: {len(chunks)}")
print("=" * 60)

# ---------------------------------------------------
# Interactive Search
# ---------------------------------------------------

while True:

    question = input("\nAsk a question (type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    results = collection.query(
        query_texts=[question],
        n_results=2
    )

    print("\n" + "=" * 60)
    print("Retrieved Results")
    print("=" * 60)

    for i in range(len(results["documents"][0])):

        print(f"\nResult {i+1}")

        print("-" * 40)

        print("Document:\n")
        print(results["documents"][0][i])

        print("\nMetadata:")
        print(results["metadatas"][0][i])

        print("\nDistance:")
        print(f"Result {i+1}")
        print(f"Similarity Distance : {results['distances'][0][i]:.3f}")
        print(f"Source              : {results['metadatas'][0][i]['source']}")
        print(f"Chunk               : {results['metadatas'][0][i]['chunk']}")
        print("\nRetrieved Context")
        print("-" * 50)
        print(results["documents"][0][i])
        print("-" * 50)

        print("-" * 40)