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


TOOL_PLANNER_PROMPT = """
You are a tool-routing assistant for an Agentic RAG system.

Use known facts and recent conversation to understand follow-up questions.

Known Long-Term Facts:
{fact_memory}

Recent Conversation:
{recent_conversation}

Choose the best tool for the current question.

Available tools:

MEMORY:
Use this when the user tells you something about themselves, their project, preferences, goals, or asks what you remember about them.

DOCUMENT_SEARCH:
Use this when the user asks about RAG, LangGraph, embeddings, ChromaDB, AI agents, uploaded documents, PDFs, notes, project knowledge, or follow-up questions about document topics.

CALCULATOR:
Use this when the user asks for arithmetic, math, percentages, numeric calculations, or expressions.

FILE_LIST:
Use this when the user asks what documents, files, PDFs, or notes are available.

DIRECT:
Use this for greetings, small talk, or simple questions that do not require tools.

Return only one of these exact words:
MEMORY
DOCUMENT_SEARCH
CALCULATOR
FILE_LIST
DIRECT

Current Question:
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


FACT_MEMORY_EXTRACTION_PROMPT = """
You are a memory extraction system.

Extract ONLY long-term facts worth remembering about the user or their project.

Save:
- User preferences
- Learning style
- Current project details
- Career goals
- Technical stack choices
- Explicit statements like "remember that..."
- Stable long-term information

Do NOT save:
- Greetings
- One-time questions
- Temporary calculations
- Random facts from assistant answers
- Full explanations
- Source citations
- Tool outputs

Return JSON only.

Format:
[
  {{
    "category": "preference | project | goal | tech_stack | learning_style | general",
    "fact": "Short fact sentence",
    "confidence": 0.95
  }}
]

If there are no facts to save, return:
[]

User Message:
{question}

Assistant Answer:
{answer}
"""
