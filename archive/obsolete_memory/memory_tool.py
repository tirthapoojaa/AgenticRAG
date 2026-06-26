from memory.fact_store import search_relevant_facts, format_facts, load_facts


def memory_tool(query: str) -> dict:
    query_lower = query.lower()

    if (
        "what do you remember" in query_lower
        or "what do you know about me" in query_lower
        or "my preferences" in query_lower
        or "about me" in query_lower
    ):
        facts = load_facts()
        result = format_facts(facts)

    else:
        result = search_relevant_facts(query, k=3)

    return {
        "tool_name": "memory",
        "result": result,
    }