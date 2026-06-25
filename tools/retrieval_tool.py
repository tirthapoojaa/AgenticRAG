from retriever import retrieve


def document_search_tool(query: str) -> dict:
    docs = retrieve(query)

    if not docs:
        return {
            "tool_name": "document_search",
            "result": "No relevant documents found.",
            "documents": []
        }

    context_parts = []
    sources = []

    for doc in docs:
        filename = doc["metadata"].get("filename", "unknown")
        chunk = doc["metadata"].get("chunk", "unknown")
        text = doc["text"]
        distance = doc.get("distance", 0)

        context_parts.append(
            f"Source: {filename}, Chunk: {chunk}\n{text}"
        )

        sources.append(
            f"- {filename}, Chunk {chunk}, Distance {distance:.4f}"
        )

    return {
        "tool_name": "document_search",
        "result": "\n\n".join(context_parts),
        "sources": "\n".join(sources),
        "documents": docs
    }