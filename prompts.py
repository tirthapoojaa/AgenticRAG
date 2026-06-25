RAG_PROMPT = """
You are a helpful AI assistant.

Use ONLY the context below to answer the user's question.

Rules:
1. If the answer is not in the context, say:
   "I don't know based on the provided documents."
2. Do not invent facts.
3. Mention the source filename when possible.

Context:
{context}

Question:
{question}

Answer:
"""