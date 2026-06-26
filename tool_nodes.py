from llm import generate_answer
from prompts import (
    TOOL_PLANNER_PROMPT,
    TOOL_ANSWER_PROMPT,
    DIRECT_PROMPT,
)
from tools.retrieval_tool import document_search_tool
from tools.calculator_tool import calculator_tool
from tools.file_tool import file_list_tool
from config import DEBUG_GRAPH


def tool_planner_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Node] Tool Planner")

    question = state["question"]
    fact_memory = state.get("fact_memory", "No saved facts.")
    recent_conversation = state.get("recent_conversation", "No recent conversation.")

    prompt = f"""
You are a tool-routing assistant for an Agentic RAG system.

Use the known facts and recent conversation to understand follow-up questions.

Known Long-Term Facts:
{fact_memory}

Recent Conversation:
{recent_conversation}

Choose the best tool for the current question.

Available tools:

MEMORY:
Use this when the user tells you something about themselves, their project, preferences, goals, or asks what you remember about them.

DOCUMENT_SEARCH:
Use this when the user asks about RAG, LangGraph, embeddings, ChromaDB, AI agents, uploaded documents, PDFs, notes, or technical project knowledge.

CALCULATOR:
Use this when the user asks for arithmetic, math, percentages, numeric calculations, or expressions.

FILE_LIST:
Use this when the user asks what documents, files, PDFs, or notes are available.

DIRECT:
Use this for greetings, small talk, or simple questions that do not require tools.

Return only one of these exact words:
MEMORY
DOCUMENT_SEARCH
CALCULATOR
FILE_LIST
DIRECT

Current Question:
{question}

Tool:
"""

    decision = generate_answer(prompt).strip().upper()

    if "MEMORY" in decision:
        tool_name = "memory"
    elif "DOCUMENT_SEARCH" in decision:
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
        "tool_input": question,
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
    fact_memory = state.get("fact_memory", "No saved facts.")
    recent_conversation = state.get("recent_conversation", "No recent conversation.")

    prompt = f"""
You are a helpful AI assistant.

Use the known facts and recent conversation if relevant.

Known Long-Term Facts:
{fact_memory}

Recent Conversation:
{recent_conversation}

Current Question:
{question}

Answer:
"""

    answer = generate_answer(prompt)
    print("\n[LLM Direct Answer]")
    print(answer)

    return {
        **state,
        "answer": answer,
    }


def tool_answer_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Node] Tool Answer")

    question = state["question"]
    tool_name = state.get("tool_name", "")
    tool_result = state.get("tool_result", "")
    sources = state.get("sources", "")
    fact_memory = state.get("fact_memory", "No saved facts.")
    recent_conversation = state.get("recent_conversation", "No recent conversation.")

    prompt = f"""
You are a helpful AI assistant.

Use the known facts, recent conversation, and tool result to answer.

Known Long-Term Facts:
{fact_memory}

Recent Conversation:
{recent_conversation}

Current Question:
{question}

Tool Used:
{tool_name}

Tool Result:
{tool_result}

Answer:
"""

    answer = generate_answer(prompt)

    if sources:
        answer = f"{answer}\n\nSources:\n{sources}"

    return {
        **state,
        "answer": answer,
    }
def memory_node(state: dict) -> dict:
    if DEBUG_GRAPH:
        print("\n[Tool] Memory")

    question = state["question"]
    fact_memory = state.get("fact_memory", "No saved facts.")
    recent_conversation = state.get("recent_conversation", "No recent conversation.")

    prompt = f"""
You are a helpful assistant with access to saved user facts.

Known Long-Term Facts:
{fact_memory}

Recent Conversation:
{recent_conversation}

Current Question:
{question}

Answer using only the saved facts and recent conversation when relevant.
If the user is sharing a new fact, acknowledge it briefly.
If there are no relevant saved facts, say that you do not have saved information yet.

Answer:
"""

    answer = generate_answer(prompt)

    return {
        **state,
        "answer": answer,
        "tool_result": fact_memory,
    }