import json
from pathlib import Path


CONVERSATION_FILE = Path("data/conversation.json")


def load_conversation() -> list[dict]:
    if not CONVERSATION_FILE.exists():
        return []

    try:
        content = CONVERSATION_FILE.read_text(encoding="utf-8")

        if not content.strip():
            return []

        return json.loads(content)

    except json.JSONDecodeError:
        return []


def save_conversation(conversation: list[dict]) -> None:
    CONVERSATION_FILE.write_text(
        json.dumps(conversation, indent=2),
        encoding="utf-8",
    )


def add_turn(role: str, content: str, limit: int = 6) -> None:
    conversation = load_conversation()

    conversation.append(
        {
            "role": role,
            "content": content,
        }
    )

    conversation = conversation[-limit:]

    save_conversation(conversation)


def format_conversation(limit: int = 6) -> str:
    conversation = load_conversation()[-limit:]

    if not conversation:
        return "No recent conversation."

    formatted = []

    for item in conversation:
        role = item.get("role", "unknown")
        content = item.get("content", "")
        formatted.append(f"{role}: {content}")

    return "\n".join(formatted)