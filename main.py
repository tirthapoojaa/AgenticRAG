from query import answer_question


def main():
    while True:
        question = input("\nAsk a question, or type 'exit': ")

        if question.lower() == "exit":
            break

        answer = answer_question(question)

        print("\nFinal Answer:")
        print(answer)


if __name__ == "__main__":
    main()