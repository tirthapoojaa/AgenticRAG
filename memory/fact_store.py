import json
from pathlib import Path


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
    FACTS_FILE.write_text(
        json.dumps(facts, indent=2),
        encoding="utf-8",
    )


def normalize_text(text: str) -> str:
    return " ".join(text.lower().strip().split())


def fact_exists(existing_facts: list[dict], new_fact: dict) -> bool:
    new_category = normalize_text(new_fact.get("category", ""))
    new_text = normalize_text(new_fact.get("fact", ""))

    for fact in existing_facts:
        old_category = normalize_text(fact.get("category", ""))
        old_text = normalize_text(fact.get("fact", ""))

        if old_category == new_category and old_text == new_text:
            return True

    return False


def add_facts(new_facts: list[dict]) -> int:
    existing_facts = load_facts()
    added_count = 0

    for fact in new_facts:
        category = fact.get("category")
        fact_text = fact.get("fact")
        confidence = fact.get("confidence", 1.0)

        if not category or not fact_text:
            continue

        if confidence < 0.6:
            continue

        clean_fact = {
            "category": category,
            "fact": fact_text,
            "confidence": confidence,
        }

        if not fact_exists(existing_facts, clean_fact):
            existing_facts.append(clean_fact)
            added_count += 1

    save_facts(existing_facts)

    return added_count


def format_facts() -> str:
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