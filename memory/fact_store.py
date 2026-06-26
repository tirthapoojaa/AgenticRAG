import json
import uuid
from pathlib import Path

from config import MEMORY_SIMILARITY_THRESHOLD
from memory.semantic_memory import (
    add_fact_to_vector_db,
    rebuild_memory_vector_db as rebuild_semantic_memory,
    search_memory,
)

FACTS_FILE = Path("data/facts.json")


def load_facts() -> list[dict]:
    if not FACTS_FILE.exists():
        return []

    try:
        content = FACTS_FILE.read_text(encoding="utf-8")

        if not content.strip():
            return []

        return json.loads(content)
    except json.JSONDecodeError:
        return []


def save_facts(facts: list[dict]) -> None:
    FACTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    FACTS_FILE.write_text(
        json.dumps(facts, indent=2),
        encoding="utf-8",
    )


def normalize_text(text: str) -> str:
    normalized = " ".join(text.lower().strip().split())

    replacements = {
        "the user's": "user",
        "user's": "user",
        "the user is": "user",
        "user is working on": "user project is",
        "user is working with": "user project is",
    }

    for old, replacement in replacements.items():
        normalized = normalized.replace(old, replacement)

    return " ".join(normalized.split())


def fact_exists(existing_facts: list[dict], new_fact: dict) -> bool:
    new_category = normalize_text(new_fact.get("category", ""))
    new_text = normalize_text(new_fact.get("fact", ""))

    for fact in existing_facts:
        old_category = normalize_text(fact.get("category", ""))
        old_text = normalize_text(fact.get("fact", ""))

        if old_category == new_category and old_text == new_text:
            return True

    return False


def find_similar_fact(new_fact_text: str) -> dict | None:
    results = search_memory(new_fact_text, k=1)

    if not results:
        return None

    best = results[0]

    if best["distance"] <= MEMORY_SIMILARITY_THRESHOLD:
        return best

    return None


def add_facts(new_facts: list[dict]) -> int:
    existing_facts = load_facts()
    changed_count = 0

    for fact in new_facts:
        category = fact.get("category")
        fact_text = fact.get("fact")
        confidence = fact.get("confidence", 1.0)

        if not category or not fact_text or confidence < 0.6:
            continue

        clean_fact = {
            "id": str(uuid.uuid4()),
            "category": category,
            "fact": fact_text,
            "confidence": confidence,
        }

        if fact_exists(existing_facts, clean_fact):
            continue

        similar = find_similar_fact(fact_text)

        if similar:
            similar_id = similar["metadata"].get("id")

            for old_fact in existing_facts:
                if old_fact.get("id") == similar_id:
                    old_fact["fact"] = fact_text
                    old_fact["category"] = category
                    old_fact["confidence"] = confidence

                    add_fact_to_vector_db(
                        fact_id=similar_id,
                        fact_text=fact_text,
                        metadata={
                            "id": similar_id,
                            "category": category,
                            "confidence": confidence,
                        },
                    )

                    changed_count += 1
                    break
        else:
            existing_facts.append(clean_fact)

            add_fact_to_vector_db(
                fact_id=clean_fact["id"],
                fact_text=fact_text,
                metadata={
                    "id": clean_fact["id"],
                    "category": category,
                    "confidence": confidence,
                },
            )

            changed_count += 1

    save_facts(existing_facts)

    return changed_count


def format_facts(facts: list[dict] | None = None) -> str:
    if facts is None:
        facts = load_facts()

    if not facts:
        return "No saved facts."

    grouped = {}

    for item in facts:
        category = item.get("category", "general")
        fact = item.get("fact", "")
        grouped.setdefault(category, []).append(fact)

    formatted = []

    for category, category_facts in grouped.items():
        formatted.append(f"{category.upper()}:")
        for fact in category_facts:
            formatted.append(f"- {fact}")

    return "\n".join(formatted)


def search_relevant_facts(query: str, k: int = 3) -> str:
    results = search_memory(query, k=k)

    if not results:
        return "No relevant saved facts."

    facts = [
        {
            "category": result["metadata"].get("category", "general"),
            "fact": result["fact"],
            "confidence": result["metadata"].get("confidence", 1.0),
        }
        for result in results
    ]

    return format_facts(facts)


def rebuild_memory_vector_db() -> None:
    facts = load_facts()

    for fact in facts:
        if "id" not in fact:
            fact["id"] = str(uuid.uuid4())

    rebuild_semantic_memory(facts)
    save_facts(facts)

    print(f"Rebuilt memory vector database with {len(facts)} facts.")
