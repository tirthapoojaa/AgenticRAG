from retriever import retrieve
from llm import generate_answer
from prompts import RAG_PROMPT
from config import SHOW_SOURCES


def build_context(retrieved_docs: list[dict]) -> str:
    context_parts = []

    for doc in retrieved_docs:
        filename = doc["metadata"].get("filename", "unknown")
        chunk = doc["metadata"].get("chunk", "unknown")
        text = doc["text"]

        context_parts.append(
            f"Source: {filename}, Chunk: {chunk}\n{text}"
        )

    return "\n\n".join(context_parts)


def build_sources(retrieved_docs: list[dict]) -> str:
    sources = []

    for doc in retrieved_docs:
        filename = doc["metadata"].get("filename", "unknown")
        chunk = doc["metadata"].get("chunk", "unknown")
        distance = doc.get("distance", 0)

        source = f"- {filename}, Chunk {chunk}, Distance {distance:.4f}"

        if source not in sources:
            sources.append(source)

    return "\n".join(sources)


def answer_question(question: str) -> str:
    retrieved_docs = retrieve(question)

    if not retrieved_docs:
        return "I could not find relevant information in the documents."

    context = build_context(retrieved_docs)

    prompt = RAG_PROMPT.format(
        context=context,
        question=question,
    )

    answer = generate_answer(prompt)

    if SHOW_SOURCES:
        sources = build_sources(retrieved_docs)
        answer = f"{answer}\n\nSources:\n{sources}"

    return answer


if __name__ == "__main__":
    while True:
        question = input("\nAsk a question, or type 'exit': ")

        if question.lower() == "exit":
            break

        answer = answer_question(question)

        print("\nAnswer:")
        print(answer)