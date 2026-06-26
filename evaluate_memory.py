import json
from pathlib import Path

from graph import run_agent


EVAL_FILE = "tests/memory_eval_questions.json"


def load_questions():
    return json.loads(Path(EVAL_FILE).read_text(encoding="utf-8"))


def check_keywords(answer: str, keywords: list[str]) -> bool:
    answer_lower = answer.lower()

    return all(keyword.lower() in answer_lower for keyword in keywords)


def evaluate_memory():
    items = load_questions()

    passed = 0
    total = len(items)

    for item in items:
        setup = item["setup"]
        follow_up = item["follow_up"]
        expected_keywords = item["expected_keywords"]

        print("\nSetup:")
        print(setup)

        run_agent(setup)

        print("\nFollow-up:")
        print(follow_up)

        answer = run_agent(follow_up)

        print("\nAnswer:")
        print(answer)

        if check_keywords(answer, expected_keywords):
            passed += 1
            print("Result: PASS")
        else:
            print("Result: FAIL")

        print("-" * 80)

    print(f"\nMemory Score: {passed}/{total}")


if __name__ == "__main__":
    evaluate_memory()
    