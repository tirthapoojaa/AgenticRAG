from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    question: str
    route: str
    tool_name: str
    tool_input: str
    tool_result: str
    retrieved_docs: List[Dict[str, Any]]
    context: str
    answer: str
    sources: str
    retry_count: int