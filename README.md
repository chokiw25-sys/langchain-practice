# LangChain Practice

A hands-on collection of small projects exploring core LangChain concepts — from a single LLM call through to retrieval-augmented generation (RAG) and custom middleware. Built while following a LangChain crash course, then extended and debugged independently.

Uses [Groq](https://groq.com) as the LLM provider (free tier, fast inference) and local, free embeddings via `sentence-transformers`.

## Setup

```bash
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
```

Create a `.env` file in the project root with your Groq API key:

```
GROQ_API_KEY=your_key_here
```

Get a free key at [console.groq.com/keys](https://console.groq.com/keys).

## Scripts

| File | Concept | Description |
|---|---|---|
| `main.py` | Basic LLM call | Simplest possible example — send one message, get one response. |
| `main2.py` | Conversation memory + streaming | Keeps a running message history so the model remembers context, and streams responses word-by-word. |
| `main3.py` | Context, structured output, memory | Uses a system prompt to set behavior, and Pydantic + `with_structured_output()` to extract structured data (task/priority/deadline) from natural language. |
| `main4.py` | Multimodal input | Chat loop that accepts an optional image alongside text, letting the model answer questions about what it sees. |
| `main5.py` | RAG (Retrieval Augmented Generation) | Loads `notes.txt`, splits it into chunks, embeds them with a local HuggingFace model, stores them in a FAISS vector store, and retrieves relevant chunks to answer questions grounded in the document. |
| `main6.py` | Dynamic system prompts | Lets the user pick a persona at runtime (tutor / code reviewer / concise assistant), changing the AI's behavior without touching the code. |
| `main7.py` | Dynamic model choice | Lets the user pick between different Groq models (fast/light, balanced, reasoning) at runtime. |
| `main8.py` | Custom middleware | Wraps the LLM call with logging, timing, and a simple content guardrail — demonstrating how production systems add safety and observability layers around model calls. |

## Notes

- `notes.txt` is sample content used by the RAG script (`main5.py`) — swap in your own document to test retrieval over different material.
- `.env` and `venv/` are gitignored and never committed.
