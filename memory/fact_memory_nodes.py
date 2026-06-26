import json
import re

from llm import generate_answer
from prompts import FACT_MEMORY_EXTRACTION_PROMPT
from memory.fact_store import format_facts, add_facts
from memory.conversation_store import format_conversation, add_turn
from config import DEBUG_GRAPH


def load_memory_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Node] Load Fact Memory")

    fact_memory = format_facts()
    recent_conversation = format_conversation(limit=2)

    if DEBUG_GRAPH:
        print("\n[Fact Memory]")
        print(fact_memory)
        print("\n[Recent Conversation]")
        print(recent_conversation)

    return {
        **state,
        "fact_memory": fact_memory,
        "recent_conversation": recent_conversation,
    }


def extract_json_array(text: str) -> list:
    """
    Handles cases where the LLM accidentally wraps JSON in text or markdown.
    """

    text = text.strip()

    text = text.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\[.*\]", text, re.DOTALL)

    if not match:
        return []

    try:
        return json.loads(match.group(0))

    except json.JSONDecodeError:
        return []


def save_fact_memory_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Node] Save Fact Memory")

    question = state.get("question", "")
    answer = state.get("answer", "")

    simple_messages = {
        "hi",
        "hello",
        "hey",
        "thanks",
        "thank you",
        "bye",
        "ok",
        "okay",
    }

    clean_question = question.strip().lower()

    add_turn("user", question)
    add_turn("assistant", answer)

    if clean_question in simple_messages:
        if DEBUG_GRAPH:
            print("[Memory] Skipping fact extraction for simple message")
        return state

    prompt = FACT_MEMORY_EXTRACTION_PROMPT.format(
        question=question,
        answer=answer,
    )

    response = generate_answer(prompt)

    extracted_facts = extract_json_array(response)

    added_count = add_facts(extracted_facts)

    if DEBUG_GRAPH:
        print(f"[Facts Extracted] {extracted_facts}")
        print(f"[Facts Added] {added_count}")

    return state