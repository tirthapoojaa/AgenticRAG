from retriever import retrieve
from llm import generate_answer
from prompts import (
    RAG_PROMPT,
    PLANNER_PROMPT,
    DIRECT_PROMPT,
    REFLECTION_PROMPT,
)
from config import DEBUG_GRAPH


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


def planner_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Node] Planner")

    question = state["question"]

    prompt = PLANNER_PROMPT.format(question=question)
    route_response = generate_answer(prompt).strip().upper()

    if "RETRIEVE" in route_response:
        route = "retrieve"
    else:
        route = "direct"

    if DEBUG_GRAPH:
        print(f"[Planner Route] {route}")

    return {
        **state,
        "route": route,
    }


def direct_answer_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Node] Direct Answer")

    question = state["question"]

    prompt = DIRECT_PROMPT.format(question=question)
    answer = generate_answer(prompt)

    return {
        **state,
        "answer": answer,
        "sources": "",
    }


def retrieval_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Node] Retrieval")

    question = state["question"]

    retrieved_docs = retrieve(question)
    context = build_context(retrieved_docs)
    sources = build_sources(retrieved_docs)

    if DEBUG_GRAPH:
        print(f"[Retrieved Chunks] {len(retrieved_docs)}")

    return {
        **state,
        "retrieved_docs": retrieved_docs,
        "context": context,
        "sources": sources,
    }


def rag_answer_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Node] RAG Answer")

    question = state["question"]
    context = state.get("context", "")

    if not context:
        return {
            **state,
            "answer": "I could not find relevant information in the documents.",
        }

    prompt = RAG_PROMPT.format(
        context=context,
        question=question,
    )

    answer = generate_answer(prompt)

    sources = state.get("sources", "")

    if sources:
        answer = f"{answer}\n\nSources:\n{sources}"

    return {
        **state,
        "answer": answer,
    }


def reflection_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Node] Reflection")

    question = state["question"]
    context = state.get("context", "")
    answer = state.get("answer", "")
    retry_count = state.get("retry_count", 0)

    prompt = REFLECTION_PROMPT.format(
        question=question,
        context=context,
        answer=answer,
    )

    decision = generate_answer(prompt).strip().upper()

    if DEBUG_GRAPH:
        print(f"[Reflection Decision] {decision}")

    if "RETRY" in decision and retry_count < 1:
        return {
            **state,
            "route": "retry",
            "retry_count": retry_count + 1,
        }

    return {
        **state,
        "route": "good",
    }