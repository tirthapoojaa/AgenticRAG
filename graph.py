from langgraph.graph import END, START, StateGraph

from memory.fact_memory_nodes import load_memory_node, save_fact_memory_node
from state import AgentState
from tool_nodes import (
    calculator_node,
    direct_node,
    document_search_node,
    file_list_node,
    memory_node,
    tool_answer_node,
    tool_planner_node,
)


def route_after_tool_planner(state: AgentState) -> str:
    tool_name = state.get("tool_name", "direct")

    if tool_name in {"document_search", "calculator", "file_list", "memory"}:
        return tool_name

    return "direct"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("load_memory", load_memory_node)
    graph.add_node("tool_planner", tool_planner_node)
    graph.add_node("document_search", document_search_node)
    graph.add_node("calculator", calculator_node)
    graph.add_node("file_list", file_list_node)
    graph.add_node("memory", memory_node)
    graph.add_node("direct", direct_node)
    graph.add_node("tool_answer", tool_answer_node)
    graph.add_node("save_fact_memory", save_fact_memory_node)

    graph.add_edge(START, "load_memory")
    graph.add_edge("load_memory", "tool_planner")

    graph.add_conditional_edges(
        "tool_planner",
        route_after_tool_planner,
        {
            "document_search": "document_search",
            "calculator": "calculator",
            "file_list": "file_list",
            "memory": "memory",
            "direct": "direct",
        },
    )

    graph.add_edge("document_search", "tool_answer")
    graph.add_edge("calculator", "tool_answer")
    graph.add_edge("file_list", "tool_answer")
    graph.add_edge("tool_answer", "save_fact_memory")
    graph.add_edge("direct", "save_fact_memory")
    graph.add_edge("memory", "save_fact_memory")
    graph.add_edge("save_fact_memory", END)

    return graph.compile()


agent_graph = build_graph()


def run_agent(question: str) -> str:
    initial_state = {
        "question": question,
        "tool_name": "",
        "tool_input": "",
        "tool_result": "",
        "retrieved_docs": [],
        "context": "",
        "answer": "",
        "sources": "",
        "recent_conversation": "",
        "fact_memory": "",
        "retry_count": 0,
    }

    final_state = agent_graph.invoke(initial_state)

    return final_state["answer"]
