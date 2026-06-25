from retriever import retrieve
from llm import generate_answer
from prompts import RAG_PROMPT


def build_context(retrieved_docs: list[dict]) -> str:
    context_parts = []

    for doc in retrieved_docs:
        source = doc["metadata"]["source"]
        chunk = doc["metadata"]["chunk"]
        text = doc["text"]

        context_parts.append(
            f"Source: {source}, Chunk: {chunk}\n{text}"
        )

    return "\n\n".join(context_parts)


def answer_question(question: str) -> str:
    retrieved_docs = retrieve(question)

    context = build_context(retrieved_docs)

    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    answer = generate_answer(prompt)

    return answer


if __name__ == "__main__":
    while True:
        question = input("\nAsk a question, or type 'exit': ")

        if question.lower() == "exit":
            break

        answer = answer_question(question)

        print("\nAnswer:")
        print(answer)