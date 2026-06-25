import json
from pathlib import Path

from graph import agent_graph


EVAL_FILE = "tests/tool_eval_questions.json"


def load_questions():
    return json.loads(Path(EVAL_FILE).read_text(encoding="utf-8"))


def run_graph_with_state(question: str):
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

    return agent_graph.invoke(initial_state)


def evaluate_tools():
    items = load_questions()

    total = len(items)
    passed = 0

    for item in items:
        question = item["question"]
        expected_tool = item["expected_tool"]

        final_state = run_graph_with_state(question)
        actual_tool = final_state.get("tool_name")

        print("\nQuestion:", question)
        print("Expected Tool:", expected_tool)
        print("Actual Tool:", actual_tool)

        if actual_tool == expected_tool:
            passed += 1
            print("Result: PASS")
        else:
            print("Result: FAIL")

        print("-" * 60)

    print(f"\nTool Routing Accuracy: {passed}/{total}")


if __name__ == "__main__":
    evaluate_tools()