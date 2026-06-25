from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    question: str
    route: str
    retrieved_docs: List[Dict[str, Any]]
    context: str
    answer: str
    sources: str
    retry_count: int