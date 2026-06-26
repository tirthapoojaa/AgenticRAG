from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    question: str

    tool_name: str
    tool_input: str
    tool_result: str

    retrieved_docs: List[Dict[str, Any]]
    context: str
    answer: str
    sources: str

    recent_conversation: str
    fact_memory: str

    retry_count: int