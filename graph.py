from langgraph.graph import StateGraph, START, END

from state import AgentState
from nodes import (
    planner_node,
    direct_answer_node,
    retrieval_node,
    rag_answer_node,
    reflection_node,
)


def route_after_planner(state: AgentState) -> str:
    route = state.get("route", "retrieve")

    if route == "direct":
        return "direct"

    return "retrieve"


def route_after_reflection(state: AgentState) -> str:
    route = state.get("route", "good")

    if route == "retry":
        return "retrieve"

    return "end"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("direct_answer", direct_answer_node)
    graph.add_node("retrieve", retrieval_node)
    graph.add_node("rag_answer", rag_answer_node)
    graph.add_node("reflect", reflection_node)

    graph.add_edge(START, "planner")

    graph.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "direct": "direct_answer",
            "retrieve": "retrieve",
        },
    )

    graph.add_edge("direct_answer", END)

    graph.add_edge("retrieve", "rag_answer")
    graph.add_edge("rag_answer", "reflect")

    graph.add_conditional_edges(
        "reflect",
        route_after_reflection,
        {
            "retrieve": "retrieve",
            "end": END,
        },
    )

    return graph.compile()


agent_graph = build_graph()


def run_agent(question: str) -> str:
    initial_state = {
        "question": question,
        "route": "",
        "retrieved_docs": [],
        "context": "",
        "answer": "",
        "sources": "",
        "retry_count": 0,
    }

    final_state = agent_graph.invoke(initial_state)

    return final_state["answer"]