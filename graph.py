from langgraph.graph import StateGraph, START, END

from state import AgentState
from tool_nodes import (
    tool_planner_node,
    document_search_node,
    calculator_node,
    file_list_node,
    direct_node,
    tool_answer_node,
)


def route_after_tool_planner(state: AgentState) -> str:
    tool_name = state.get("tool_name", "direct")

    if tool_name == "document_search":
        return "document_search"

    if tool_name == "calculator":
        return "calculator"

    if tool_name == "file_list":
        return "file_list"

    return "direct"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("tool_planner", tool_planner_node)
    graph.add_node("document_search", document_search_node)
    graph.add_node("calculator", calculator_node)
    graph.add_node("file_list", file_list_node)
    graph.add_node("direct", direct_node)
    graph.add_node("tool_answer", tool_answer_node)

    graph.add_edge(START, "tool_planner")

    graph.add_conditional_edges(
        "tool_planner",
        route_after_tool_planner,
        {
            "document_search": "document_search",
            "calculator": "calculator",
            "file_list": "file_list",
            "direct": "direct",
        }
    )

    graph.add_edge("document_search", "tool_answer")
    graph.add_edge("calculator", "tool_answer")
    graph.add_edge("file_list", "tool_answer")

    graph.add_edge("direct", END)
    graph.add_edge("tool_answer", END)

    return graph.compile()


agent_graph = build_graph()


def run_agent(question: str) -> str:
    initial_state = {
        "question": question,
        "route": "",
        "tool_name": "",
        "tool_input": "",
        "tool_result": "",
        "retrieved_docs": [],
        "context": "",
        "answer": "",
        "sources": "",
        "retry_count": 0,
    }

    final_state = agent_graph.invoke(initial_state)

    return final_state["answer"]