RAG_PROMPT = """
You are a helpful AI assistant.

Answer the question using ONLY the context provided below.
If the answer is not present in the context, say:
"I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""