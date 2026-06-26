import json
from pathlib import Path


MEMORY_FILE = Path("memory_store.json")


def load_memory() -> list[dict]:
    if not MEMORY_FILE.exists():
        return []

    try:
        content = MEMORY_FILE.read_text(encoding="utf-8")

        if not content.strip():
            return []

        return json.loads(content)

    except json.JSONDecodeError:
        return []


def save_memory(memory: list[dict]) -> None:
    MEMORY_FILE.write_text(
        json.dumps(memory, indent=2),
        encoding="utf-8"
    )


def add_memory(role: str, content: str) -> None:
    memory = load_memory()

    memory.append(
        {
            "role": role,
            "content": content
        }
    )

    save_memory(memory)


def get_recent_memory(limit: int = 6) -> list[dict]:
    memory = load_memory()

    return memory[-limit:]


def format_memory(memory_items: list[dict]) -> str:
    if not memory_items:
        return "No previous memory."

    formatted = []

    for item in memory_items:
        role = item.get("role", "unknown")
        content = item.get("content", "")

        formatted.append(f"{role}: {content}")

    return "\n".join(formatted)