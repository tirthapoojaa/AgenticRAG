from llm import generate_answer
from prompts import TOOL_PLANNER_PROMPT, TOOL_ANSWER_PROMPT, DIRECT_PROMPT
from tools.retrieval_tool import document_search_tool
from tools.calculator_tool import calculator_tool
from tools.file_tool import file_list_tool
from config import DEBUG_GRAPH


def tool_planner_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Node] Tool Planner")

    question = state["question"]

    prompt = TOOL_PLANNER_PROMPT.format(question=question)
    decision = generate_answer(prompt).strip().upper()

    if "DOCUMENT_SEARCH" in decision:
        tool_name = "document_search"
    elif "CALCULATOR" in decision:
        tool_name = "calculator"
    elif "FILE_LIST" in decision:
        tool_name = "file_list"
    else:
        tool_name = "direct"

    if DEBUG_GRAPH:
        print(f"[Selected Tool] {tool_name}")

    return {
        **state,
        "tool_name": tool_name,
        "tool_input": question
    }


def document_search_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Tool] Document Search")

    question = state["question"]

    result = document_search_tool(question)

    return {
        **state,
        "tool_result": result["result"],
        "retrieved_docs": result.get("documents", []),
        "context": result["result"],
        "sources": result.get("sources", "")
    }


def calculator_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Tool] Calculator")

    question = state["question"]

    result = calculator_tool(question)

    return {
        **state,
        "tool_result": result["result"]
    }


def file_list_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Tool] File List")

    result = file_list_tool()

    return {
        **state,
        "tool_result": result["result"]
    }


def direct_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Node] Direct Answer")

    question = state["question"]

    prompt = DIRECT_PROMPT.format(question=question)
    answer = generate_answer(prompt)

    return {
        **state,
        "answer": answer
    }


def tool_answer_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Node] Tool Answer")

    question = state["question"]
    tool_name = state.get("tool_name", "")
    tool_result = state.get("tool_result", "")
    sources = state.get("sources", "")

    prompt = TOOL_ANSWER_PROMPT.format(
        question=question,
        tool_name=tool_name,
        tool_result=tool_result
    )

    answer = generate_answer(prompt)

    if sources:
        answer = f"{answer}\n\nSources:\n{sources}"

    return {
        **state,
        "answer": answer
    }