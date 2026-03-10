# 🤖 Agentic RAG over Complex Real-World Documents

A fully local, multi-agent RAG (Retrieval-Augmented Generation) system that lets you chat with any PDF using AI agents. Built with CrewAI, GroundX, DeepSeek-R1, and Streamlit.

---

## 🧠 How It Works

Two AI agents collaborate sequentially to answer your questions:

```
You ask a question
       ↓
  Retriever Agent
  ├── searches your PDF first (via GroundX)
  └── falls back to web search (via Serper) if needed
       ↓
  Synthesizer Agent
  └── formats a clean, coherent answer
       ↓
  Streamlit Chat UI
```

**Why two agents?** The Retriever focuses purely on finding relevant information, while the Synthesizer focuses purely on communicating it clearly. Two specialized agents produce better answers than a single monolithic prompt.

---

## 🛠️ Tech Stack

| Component | Tool | Purpose |
|---|---|---|
| Agent Orchestration | [CrewAI](https://crewai.com) | Coordinates multiple AI agents |
| Document Parsing | [GroundX](https://eyelevel.ai) | Enterprise-grade PDF parsing & retrieval |
| LLM | [DeepSeek-R1:7b](https://ollama.com/library/deepseek-r1) via Ollama | Local language model, no API costs |
| Web Search Fallback | [Serper](https://serper.dev) | Google Search API for queries outside the PDF |
| UI | [Streamlit](https://streamlit.io) | Chat interface |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.com) installed

### 1. Clone the repo
```bash
git clone https://github.com/yashmundhe/agentic-rag-deepseek.git
cd agentic-rag-deepseek
```

### 2. Install Ollama and pull DeepSeek
```bash
# Install Ollama (Mac)
brew install ollama

# Start Ollama server (keep this running)
ollama serve

# In a new terminal, pull the model (~4.7GB)
ollama pull deepseek-r1:7b
```

### 3. Install Python dependencies
```bash
pip install groundx crewai crewai-tools streamlit python-dotenv litellm anthropic
```

### 4. Set up API keys
Create a `.env` file in the project root:
```
GROUNDX_API_KEY=your_groundx_key_here
SERPER_API_KEY=your_serper_key_here
```

Get your keys:
- [GroundX API key](https://docs.eyelevel.ai/documentation/fundamentals/quickstart#step-1-getting-your-api-key)
- [Serper API key](https://serper.dev)

### 5. Run the app
```bash
streamlit run app_deep_seek.py
```

---

## 📁 Project Structure

```
agentic_rag_deepseek/
├── app_deep_seek.py          # Main Streamlit app
├── assets/                   # Images
├── knowledge/                # Sample PDFs
├── src/agentic_rag/
│   ├── config/
│   │   ├── agents.yaml       # Agent definitions
│   │   └── tasks.yaml        # Task definitions
│   ├── tools/
│   │   └── custom_tool.py    # GroundX document search tool
│   ├── crew.py               # CrewAI crew definition
│   └── main.py               # CLI entry point
└── .env                      # API keys (not committed)
```

---

## ⚙️ Key Design Decisions

**Why GroundX over basic PDF readers?** Standard PDF parsers like PyPDF2 struggle with complex layouts, tables, and charts. GroundX uses computer vision to parse documents the way a human would read them, resulting in much better retrieval quality.

**Why local LLM?** Running DeepSeek-R1:7b via Ollama means zero API costs and full data privacy — your documents never leave your machine.

**Why CrewAI?** Splitting retrieval and synthesis into separate agents with distinct roles produces more reliable, higher-quality answers compared to a single monolithic prompt.

---

## 🔧 Troubleshooting

**`Connection refused` error** — Ollama server isn't running. Start it with `ollama serve`.

**Slow responses** — Expected with a 7B model locally. For faster responses, swap to `deepseek-r1:1.5b` in `app_deep_seek.py`.

**Document still processing** — GroundX takes 30–60 seconds to index a new PDF. Wait and retry your query.

**`litellm` not found** — Run `pip install litellm`.

---

## 📬 Connect

Built by [Yash Mundhe](https://www.linkedin.com/in/yashmundhe) — MS Data Science @ Northeastern University

Interested in data engineering, agentic AI, and building things that actually work.
