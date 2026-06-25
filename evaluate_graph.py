import json
from pathlib import Path

from graph import agent_graph


EVAL_FILE = "tests/graph_eval_questions.json"


def load_questions():
    return json.loads(Path(EVAL_FILE).read_text(encoding="utf-8"))


def run_graph_with_state(question: str):
    initial_state = {
        "question": question,
        "route": "",
        "retrieved_docs": [],
        "context": "",
        "answer": "",
        "sources": "",
        "retry_count": 0,
    }

    return agent_graph.invoke(initial_state)


def evaluate_routes():
    items = load_questions()

    total = len(items)
    passed = 0

    for item in items:
        question = item["question"]
        expected_route = item["expected_route"]

        final_state = run_graph_with_state(question)

        actual_route = "retrieve" if final_state.get("retrieved_docs") else "direct"

        print("\nQuestion:", question)
        print("Expected:", expected_route)
        print("Actual:", actual_route)

        if actual_route == expected_route:
            passed += 1
            print("Result: PASS")
        else:
            print("Result: FAIL")

        print("-" * 60)

    print(f"\nRoute Accuracy: {passed}/{total}")


if __name__ == "__main__":
    evaluate_routes()