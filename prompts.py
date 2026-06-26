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

MEMORY_AWARE_TOOL_PLANNER_PROMPT = """
You are a tool-routing assistant for an Agentic RAG system.

Use the conversation memory to understand follow-up questions.

Conversation Memory:
{memory}

Choose the best tool for the current question.

Available tools:

DOCUMENT_SEARCH:
Use this when the user asks about RAG, LangGraph, embeddings, ChromaDB, AI agents, uploaded documents, PDFs, notes, project knowledge, or follow-up questions about previously discussed document topics.

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

Current Question:
{question}

Tool:
"""


MEMORY_AWARE_TOOL_ANSWER_PROMPT = """
You are a helpful AI assistant.

Use the conversation memory and tool result to answer the user's question.

Conversation Memory:
{memory}

Current Question:
{question}

Tool Used:
{tool_name}

Tool Result:
{tool_result}

Answer:
"""


MEMORY_SAVE_PROMPT = """
You are a memory manager.

Decide whether the following user message contains useful information that should be saved for future conversations.

Save information if it includes:
- User preferences
- User project details
- User learning goals
- Important facts the user explicitly wants remembered
- Ongoing project decisions

Do NOT save:
- Greetings
- Random one-time questions
- Temporary calculations
- Short acknowledgements

Return only one word:
SAVE or IGNORE

User Message:
{question}

Assistant Answer:
{answer}

Decision:
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


MEMORY_CONTEXT_PROMPT = """
Known Long-Term Facts:
{fact_memory}

Recent Conversation:
{recent_conversation}

Current Question:
{question}
"""