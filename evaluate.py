import json
from pathlib import Path

from query import answer_question


EVAL_FILE = "tests/eval_questions.json"


def load_eval_questions():
    path = Path(EVAL_FILE)

    if not path.exists():
        raise FileNotFoundError(
            f"{EVAL_FILE} not found. Create it before running evaluation."
        )

    return json.loads(path.read_text(encoding="utf-8"))


def check_keywords(answer: str, keywords: list[str]) -> bool:
    answer_lower = answer.lower()

    return all(
        keyword.lower() in answer_lower
        for keyword in keywords
    )


def run_evaluation():
    questions = load_eval_questions()

    total = len(questions)
    passed = 0

    for item in questions:
        question = item["question"]
        expected_keywords = item["expected_keywords"]

        print("\nQuestion:")
        print(question)

        answer = answer_question(question)

        print("\nAnswer:")
        print(answer)

        is_correct = check_keywords(answer, expected_keywords)

        if is_correct:
            passed += 1
            print("\nResult: PASS")
        else:
            print("\nResult: FAIL")
            print("Expected keywords:", expected_keywords)

        print("-" * 80)

    print("\nEvaluation Summary")
    print(f"Passed: {passed}/{total}")
    print(f"Score: {(passed / total) * 100:.2f}%")


if __name__ == "__main__":
    run_evaluation()