RAG_PROMPT = """
You are a helpful AI assistant.

Use ONLY the retrieved context to answer the user's question.

Rules:
1. You may combine information from multiple retrieved chunks.
2. If the answer is not directly stated but can be logically inferred from the context, explain the inference.
3. Do not use outside knowledge.
4. Do not invent facts.
5. Mention source filenames when useful.
6. If the context is genuinely insufficient, say:
   "I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

PLANNER_PROMPT = """
You are a routing assistant for a RAG system.

Decide whether the user's question needs document retrieval.

Return only one word:

RETRIEVE - if the question asks about RAG, LangGraph, embeddings, ChromaDB, AI agents, the user's notes, documents, or technical project content.

DIRECT - if the question is only a greeting, small talk, or does not require document knowledge.

Question:
{question}

Route:
"""


DIRECT_PROMPT = """
You are a helpful assistant.

Answer the user's message naturally and briefly.

User:
{question}

Answer:
"""


REFLECTION_PROMPT = """
You are checking whether an answer is supported by the retrieved context.

Return only one word:

GOOD - if the answer is supported by the context.
RETRY - if the answer says it does not know, or if the answer seems incomplete even though the context contains useful information.

Question:
{question}

Context:
{context}

Answer:
{answer}

Decision:
"""
TOOL_PLANNER_PROMPT = """
You are a tool-routing assistant for an Agentic RAG system.

Choose the best tool for the user's question.

Available tools:

DOCUMENT_SEARCH:
Use this when the user asks about RAG, LangGraph, embeddings, ChromaDB, AI agents, uploaded documents, PDFs, notes, or project knowledge.

CALCULATOR:
Use this when the user asks for arithmetic, math, percentages, numeric calculations, or expressions.

FILE_LIST:
Use this when the user asks what documents, files, PDFs, or notes are available.

DIRECT:
Use this for greetings, small talk, or questions that do not require a tool.

Return only one of these exact words:
DOCUMENT_SEARCH
CALCULATOR
FILE_LIST
DIRECT

Question:
{question}

Tool:
"""


TOOL_ANSWER_PROMPT = """
You are a helpful AI assistant.

Answer the user's question using the tool result below.

Question:
{question}

Tool Used:
{tool_name}

Tool Result:
{tool_result}

Answer:
"""