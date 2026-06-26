from llm import generate_answer
from prompts import MEMORY_SAVE_PROMPT
from memory.memory_store import (
    get_recent_memory,
    format_memory,
    add_memory,
)
from config import DEBUG_GRAPH


def load_memory_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Node] Load Memory")

    recent_memory = get_recent_memory(limit=8)
    formatted_memory = format_memory(recent_memory)

    if DEBUG_GRAPH:
        print("[Memory Loaded]")
        print(formatted_memory)

    return {
        **state,
        "conversation_history": recent_memory,
        "relevant_memory": formatted_memory,
    }


def save_memory_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Node] Save Memory")

    question = state.get("question", "")
    answer = state.get("answer", "")

    prompt = MEMORY_SAVE_PROMPT.format(
        question=question,
        answer=answer,
    )

    decision = generate_answer(prompt).strip().upper()

    if DEBUG_GRAPH:
        print(f"[Memory Decision] {decision}")

    # Always save the conversation turn for short-term continuity
    if "SAVE" in decision:
        add_memory("user", question)
        add_memory("assistant", answer)

    return state