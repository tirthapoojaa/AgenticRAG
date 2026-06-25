from query import answer_question


def main():
    print("Personal Notes RAG System")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nAsk a question: ")

        if question.lower() == "exit":
            break

        answer = answer_question(question)

        print("\nFinal Answer:")
        print(answer)


if __name__ == "__main__":
    main()