# AgenticRAG

> An intelligent Retrieval-Augmented Generation (RAG) system built with **LangGraph**, **ChromaDB**, **Groq LLM**, and **semantic long-term memory**.

---

## Overview

AgenticRAG is an AI assistant capable of intelligently answering questions over a personal knowledge base while maintaining persistent user memory.

Unlike a traditional RAG pipeline, this project uses **LangGraph** to orchestrate an agentic workflow with multiple tools, planning, retrieval, and memory management.

The system combines:

* Retrieval-Augmented Generation (RAG)
* Agentic workflows
* Tool routing
* Semantic search
* Persistent fact-based memory
* Conversation memory

to create a modular AI assistant architecture.

---

# Features

### Agentic Workflow (LangGraph)

* Graph-based execution using LangGraph
* Conditional tool routing
* Stateful execution
* Modular node architecture

---

### Retrieval-Augmented Generation (RAG)

* Semantic document retrieval
* ChromaDB vector database
* BGE embeddings
* Context-grounded responses
* Hallucination reduction

---

### Tool Calling

The planner dynamically selects the most appropriate tool.

Available tools:

* Document Search
* Calculator
* File Listing
* Memory Tool
* Direct Response

---

### Long-Term Memory

Persistent user memory stored across sessions.

Stores:

* User preferences
* Current projects
* Career goals
* Learning preferences
* Technical stack
* Long-term facts

Does **not** store:

* Greetings
* Temporary questions
* Random conversations
* One-time responses

---

### Short-Term Memory

Conversation history is maintained separately from long-term memory.

Used for:

* Follow-up questions
* Multi-turn conversations
* Context continuity

---

### Semantic Memory Retrieval

Instead of loading every stored fact into every prompt, the system:

Question

↓

Embedding

↓

Semantic Search

↓

Relevant Facts

↓

LLM

This greatly reduces token usage while improving relevance.

---

## Project Architecture

```text
                   User
                     │
                     ▼
              LangGraph Agent
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   Load Fact Memory      Recent Conversation
          │                     │
          └──────────┬──────────┘
                     ▼
               Tool Planner
                     │
 ┌──────────┬────────┼─────────┬───────────┐
 ▼          ▼        ▼         ▼
Memory   Retriever Calculator File Tool
 Tool
 │          │        │         │
 └──────────┴────────┴─────────┘
                     │
                     ▼
               Tool Answer
                     │
                     ▼
          Save Fact Memory
                     │
                     ▼
                   Output
```

---

# Technologies Used

| Technology             | Purpose                       |
| ---------------------- | ----------------------------- |
| Python                 | Core application              |
| LangGraph              | Agent workflow orchestration  |
| ChromaDB               | Vector database               |
| Groq                   | LLM inference                 |
| SentenceTransformers   | Embedding generation          |
| BAAI/bge-small-en-v1.5 | Embedding model               |
| LangChain              | Document processing utilities |

---

# Folder Structure

```text
AgenticRAG/

├── config.py
├── main.py
├── graph.py
├── llm.py
├── database.py
├── retriever.py
├── prompts.py
├── ingest.py
│
├── tools/
│   ├── calculator_tool.py
│   ├── retrieval_tool.py
│   ├── file_tool.py
│   └── memory_tool.py
│
├── memory/
│   ├── conversation_store.py
│   ├── fact_store.py
│   ├── semantic_memory.py
│   └── fact_memory_nodes.py
│
├── docs/
├── data/
├── db/
└── requirements.txt
```

---

# Workflow

## Document Ingestion

```
Documents

↓

Chunking

↓

Embedding Model

↓

Vector Embeddings

↓

ChromaDB
```

---

## Query Flow

```
User Question

↓

Load Memory

↓

Planner

↓

Select Tool

↓

Execute Tool

↓

Generate Answer

↓

Extract Facts

↓

Persist Memory
```

---

# Memory System

The project uses two complementary memory systems.

## Conversation Memory

Maintains recent conversation history.

Purpose:

* Multi-turn dialogue
* Context preservation
* Follow-up questions

---

## Fact Memory

Stores long-term information only.

Example:

```
Project:
Building an Agentic RAG system using LangGraph.

Preference:
Prefers Python examples.

Goal:
Become an AI Engineer.
```

Facts are retrieved semantically using vector search rather than loading every stored fact.

---

# Tool Routing

The planner dynamically selects the correct tool.

| User Query                       | Selected Tool   |
| -------------------------------- | --------------- |
| "What is LangGraph?"             | Document Search |
| "25 * 18"                        | Calculator      |
| "What files do you have?"        | File Tool       |
| "What do you remember about me?" | Memory Tool     |
| "Hi"                             | Direct Response |

---

# Running the Project

## Clone

```bash
git clone https://github.com/<your-username>/AgenticRAG.git

cd AgenticRAG
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate

macOS/Linux

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file

```env
GROQ_API_KEY=YOUR_API_KEY
```

---

## Ingest Documents

Place your `.txt` or `.pdf` files inside the `docs/` directory.

Run:

```bash
python ingest.py
```

---

## Start the Agent

```bash
python main.py
```

---

# Example

```
Ask a question:

What is LangGraph?
```

↓

Planner

↓

Retriever

↓

Grounded Answer

---

```
Ask a question:

My project is an Agentic RAG system using LangGraph.
```

↓

Memory Tool

↓

Fact Extraction

↓

Persistent Memory

---

```
Ask a question:

What do you remember about me?
```

↓

Semantic Memory Retrieval

↓

Personalized Answer

---

# Future Improvements

* Reflection & self-correction
* Multi-step planning
* Web search integration
* Hybrid retrieval (BM25 + Vector Search)
* Streaming responses
* FastAPI deployment
* Web interface
* Automated evaluation framework
* Memory consolidation
* Multi-agent collaboration

---

# Learning Outcomes

This project demonstrates practical implementation of:

* Retrieval-Augmented Generation (RAG)
* LangGraph workflows
* Tool Calling
* Semantic Search
* Vector Databases
* Embeddings
* Persistent Memory
* Agentic AI
* State Machines
* Modular AI Architecture

---

# Author

**Tirthapooja N**

B.Tech Artificial Intelligence & Data Science

Passionate about Generative AI, Agentic AI, LLM Systems, and AI Infrastructure.
