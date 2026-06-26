from memory.fact_store import format_facts, load_facts, search_relevant_facts


def memory_tool(query: str) -> dict:
    query_lower = query.lower()

    if (
        "what do you remember" in query_lower
        or "what do you know about me" in query_lower
        or "about me" in query_lower
        or "my preferences" in query_lower
    ):
        result = format_facts(load_facts())
    else:
        result = search_relevant_facts(query)

    return {
        "tool_name": "memory",
        "result": result,
    }
