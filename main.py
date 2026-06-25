from graph import run_agent


def main():
    print("Agentic RAG System with LangGraph")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nAsk a question: ")

        if question.lower() == "exit":
            break

        answer = run_agent(question)

        print("\nFinal Answer:")
        print(answer)


if __name__ == "__main__":
    main()