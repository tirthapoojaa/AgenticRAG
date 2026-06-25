from llm import generate_answer

question = "What is Retrieval-Augmented Generation (RAG)?"

try:
    response = generate_answer(question)

    print("✅ Connected to Groq successfully!\n")
    print(response)

except Exception as e:
    print("❌ Connection failed")
    print(e)