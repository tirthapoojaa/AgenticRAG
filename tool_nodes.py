from llm import generate_answer
from prompts import TOOL_PLANNER_PROMPT
from tools.retrieval_tool import document_search_tool
from tools.calculator_tool import calculator_tool
from tools.file_tool import file_list_tool
from tools.memory_tool import memory_tool
from config import DEBUG_GRAPH


def _debug(message: str) -> None:
    if DEBUG_GRAPH:
        print(message)


def _select_tool(decision: str) -> str:
    decision = decision.strip().upper()

    if "DOCUMENT_SEARCH" in decision:
        return "document_search"
    if "CALCULATOR" in decision:
        return "calculator"
    if "FILE_LIST" in decision:
        return "file_list"
    if "MEMORY" in decision:
        return "memory"
    return "direct"


def tool_planner_node(state: dict) -> dict:
    _debug("\n[Node] Tool Planner")

    question = state["question"]
    prompt = TOOL_PLANNER_PROMPT.format(
        question=question,
        fact_memory=state.get("fact_memory", "No saved facts."),
        recent_conversation=state.get("recent_conversation", "No recent conversation."),
    )

    decision = generate_answer(prompt)
    tool_name = _select_tool(decision)

    _debug(f"[Selected Tool] {tool_name}")

    return {
        **state,
        "tool_name": tool_name,
        "tool_input": question,
    }


def document_search_node(state: dict) -> dict:
    _debug("\n[Tool] Document Search")

    result = document_search_tool(state["question"])

    return {
        **state,
        "tool_result": result["result"],
        "retrieved_docs": result.get("documents", []),
        "context": result["result"],
        "sources": result.get("sources", ""),
    }


def calculator_node(state: dict) -> dict:
    _debug("\n[Tool] Calculator")

    result = calculator_tool(state["question"])

    return {
        **state,
        "tool_result": result["result"],
    }


def file_list_node(state: dict) -> dict:
    _debug("\n[Tool] File List")

    result = file_list_tool()

    return {
        **state,
        "tool_result": result["result"],
    }


def memory_node(state: dict) -> dict:
    _debug("\n[Tool] Memory")

    result = memory_tool(state["question"])

    prompt = f"""
You are a helpful assistant with access to saved user facts.

Relevant Saved Facts:
{result["result"]}

Recent Conversation:
{state.get("recent_conversation", "No recent conversation.")}

Current Question:
{state["question"]}

Answer naturally using only the saved facts when relevant.
If the user is sharing a new fact, acknowledge it briefly.
If there are no relevant saved facts, say you do not have saved information yet.

Answer:
"""

    answer = generate_answer(prompt)

    return {
        **state,
        "tool_result": result["result"],
        "answer": answer,
    }


def direct_node(state: dict) -> dict:
    _debug("\n[Node] Direct Answer")

    prompt = f"""
You are a helpful AI assistant.

Use known facts and recent conversation only when they are relevant.

Known Long-Term Facts:
{state.get("fact_memory", "No saved facts.")}

Recent Conversation:
{state.get("recent_conversation", "No recent conversation.")}

Current Question:
{state["question"]}

Answer naturally and briefly.

Answer:
"""

    answer = generate_answer(prompt)

    return {
        **state,
        "answer": answer,
    }


def tool_answer_node(state: dict) -> dict:
    _debug("\n[Node] Tool Answer")

    prompt = f"""
You are a helpful AI assistant.

Use the known facts, recent conversation, and tool result to answer.

Known Long-Term Facts:
{state.get("fact_memory", "No saved facts.")}

Recent Conversation:
{state.get("recent_conversation", "No recent conversation.")}

Current Question:
{state["question"]}

Tool Used:
{state.get("tool_name", "")}

Tool Result:
{state.get("tool_result", "")}

Answer:
"""

    answer = generate_answer(prompt)
    sources = state.get("sources", "")

    if sources:
        answer = f"{answer}\n\nSources:\n{sources}"

    return {
        **state,
        "answer": answer,
    }
