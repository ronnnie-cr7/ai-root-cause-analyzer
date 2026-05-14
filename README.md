# 🔍 AI Root Cause Analyzer

An Agentic AI system that validates, routes, and analyzes system logs using a multi-agent LangGraph architecture with confidence-based decision making, web search fallback, human-in-the-loop, and persistent memory.

Built with LangGraph, LangChain, Groq, ChromaDB, FastAPI, and Streamlit.

## 🌐 Live Demo

- **Frontend:** https://ai-root-cause-analyzer.streamlit.app
- **API Docs:** https://ronityadav8905-ai-root-cause-analyzer-api.hf.space/docs

---

## 🏗️ Agentic Architecture

```
Input → [Validator] → [Log Parser] → [Router] → [Anomaly Detector] → [RAG Agent]
                                                                           ↓
                                                                   [Root Cause Agent]
                                                                           ↓
                                                                  [Confidence Checker]
                                                              ↙         ↓           ↘
                                                        score<80   score<60       score≥80
                                                      loop back   ask human      [Fix Agent]
                                                      to RAG      for context        ↓
                                                    (max 3 attempts)             Final Report
                                                                                      ↓
                                                                               [SQLite Memory]
```

This is a true agentic system — not a fixed pipeline:
- **Validates** input before wasting API calls
- **Routes** based on severity (CRITICAL / HIGH / LOW)
- **Loops back** if confidence is too low
- **Falls back to web search** if RAG similarity < 0.6
- **Asks a human** when stuck after 3 attempts
- **Remembers** all past analyses in SQLite

---

## 🤖 Agents

| Agent | Job |
|---|---|
| Validator | Rejects invalid input before any LLM calls |
| Log Parser | Structures raw messy logs into clean data |
| Router | Decides severity and analysis depth |
| Anomaly Detector | Finds patterns, severity, and confidence score |
| RAG Agent | Searches ChromaDB or web depending on similarity score |
| Root Cause Analyzer | Synthesizes everything into a definitive root cause |
| Confidence Checker | Loops back, asks human, or proceeds based on confidence |
| Fix Suggester | Provides immediate, short term, and long term fixes |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Multi-Agent Orchestration | LangGraph with conditional edges |
| LLM | Groq (Llama 3.3 70B) |
| RAG + Chains | LangChain |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2) |
| Vector Memory | ChromaDB — 30 past incidents |
| Web Search Fallback | DuckDuckGo Search |
| Persistent Memory | SQLite |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Deployment | Docker + Hugging Face Spaces + Streamlit Cloud |

---

## 🚀 Running Locally

### 1. Clone the repo
```bash
git clone https://github.com/ronnnie-cr7/ai-root-cause-analyzer
cd ai-root-cause-analyzer
```

### 2. Add your Groq API key
```bash
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

### 3. Seed the vector database
```bash
python -m rag.vectorstore
```

### 4. Run with Docker
```bash
docker-compose up --build
```

- API: http://localhost:8000/docs
- Frontend: http://localhost:8501

### 5. Live Deployment
- **Frontend:** Streamlit Community Cloud
- **Backend API:** Hugging Face Spaces (Docker) — no cold starts, runs 24/7

---

## 📸 Demo Flow

1. Click a sample log button (Python, Nginx, or Kubernetes)
2. Watch 8 agents run with live status updates
3. System validates, routes by severity, analyzes with confidence scoring
4. If RAG similarity < 0.6 — agent searches the web automatically
5. If confidence < 60 after 3 attempts — agent asks you for more context
6. Download the full report, check Memory tab for history

---

## ✨ Features

- **Input validation** — rejects garbage before wasting API calls
- **Severity routing** — CRITICAL / HIGH / LOW with visual badges
- **Confidence loop** — re-analyzes if confidence below 80%
- **Web search fallback** — DuckDuckGo search when RAG score < 0.6
- **Human in the loop** — asks engineer for context when stuck after 3 attempts
- **Persistent memory** — SQLite stores all analyses across sessions
- **Memory tab** — view history, total analyses, avg confidence
- **3 sample log types** — Python, Nginx, Kubernetes
- **Semantic RAG** — SentenceTransformer embeddings, 0.7+ scores
- **Download report** — export full analysis as text file

---

## 📁 Project Structure

```
ai-root-cause-analyzer/
├── agents/
│   ├── validator_agent.py       # Input guardrail
│   ├── log_parser_agent.py      # Log structuring
│   ├── router_agent.py          # Severity routing
│   ├── anomaly_agent.py         # Pattern detection
│   ├── rag_agent.py             # ChromaDB + web search fallback
│   ├── root_cause_agent.py      # Root cause synthesis
│   ├── confidence_checker.py    # Loop/human/proceed decision
│   └── fix_agent.py             # Fix suggestions
├── graph/
│   └── workflow.py              # LangGraph with conditional edges
├── rag/
│   ├── vectorstore.py           # ChromaDB setup
│   ├── memory.py                # SQLite persistent memory
│   └── seed_incidents.py        # Incident seeder
├── api/main.py                  # FastAPI backend
├── frontend/app.py              # Streamlit UI
├── data/
│   ├── past_incidents.json      # 30 historical incidents
│   └── sample_logs/             # Sample log files
└── config/settings.py           # API keys and settings
```

---

## 💡 Key Design Decisions

- **True agentic over fixed pipeline** — conditional edges, confidence loops, human escalation
- **Web search fallback** — agent is not limited to internal knowledge
- **Human in the loop** — agent knows when it doesn't know, escalates to engineer
- **SQLite memory** — zero infrastructure, persistent across sessions
- **Validator guardrail** — invalid input rejected before any LLM calls
- **SentenceTransformer embeddings** — 0.7+ similarity vs 0.1 with defaults
- **HF Spaces deployment** — no cold starts, no spin downs, runs 24/7 for free

---

## 🔮 Future Improvements

- Parallel agents for faster analysis
- Slack/PagerDuty integration for real-time alerting
- Auto-add resolved incidents to ChromaDB so RAG gets smarter over time
- Fine-tune on real incident data
- Voice interface
