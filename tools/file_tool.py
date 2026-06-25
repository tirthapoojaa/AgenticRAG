from pathlib import Path
from config import DOCS_PATH


def file_list_tool() -> dict:
    docs_dir = Path(DOCS_PATH)

    if not docs_dir.exists():
        return {
            "tool_name": "file_lister",
            "result": f"Documents folder '{DOCS_PATH}' does not exist."
        }

    supported_extensions = {".txt", ".md", ".pdf"}

    files = [
        file.name
        for file in docs_dir.rglob("*")
        if file.is_file() and file.suffix.lower() in supported_extensions
    ]

    if not files:
        return {
            "tool_name": "file_lister",
            "result": "No supported documents found."
        }

    file_list = "\n".join(f"- {file}" for file in files)

    return {
        "tool_name": "file_lister",
        "result": file_list
    }