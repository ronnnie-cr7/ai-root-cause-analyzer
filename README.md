# AI Root Cause Analyzer

> **SRE teams spend 40–60 minutes triaging a single incident. This does it in seconds — with confidence scoring, web search fallback, and human escalation when it's genuinely uncertain.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=flat-square&logo=streamlit)](https://ai-root-cause-analyzer.streamlit.app)
[![API Docs](https://img.shields.io/badge/API%20Docs-FastAPI-009688?style=flat-square&logo=fastapi)](https://ronityadav8905-ai-root-cause-analyzer-api.hf.space/docs)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic-orange?style=flat-square)](https://python.langchain.com/langgraph/)

---

## The Problem

When a production system goes down, engineers don't have time to read through 500 lines of logs, cross-reference past incidents, and reason about root causes under pressure. Most teams either spend too long triaging or make confident-sounding guesses.

This system automates that process — not with a fixed pipeline that pretends it always knows the answer, but with an agent that **knows when it doesn't know** and handles that case explicitly.

---

## What Makes This Different From a Standard RAG Chatbot

Most "agentic AI" projects are just LLM calls dressed up with a loop. This one has genuine decision-making:

- **Confidence loops** — if the analysis confidence is below 90%, the agent re-runs RAG automatically (up to 3 attempts)
- **Web search fallback** — if RAG similarity drops below 0.6, the agent searches the web rather than hallucinating from internal knowledge
- **Human escalation** — if 3 attempts still don't yield confidence above 85%, the agent asks the engineer for more context instead of guessing
- **Input guardrail** — a validator agent rejects garbage input before any LLM calls are made, saving API cost

This is the architecture a real SRE tool would need, not a demo that only works on clean inputs.

---

## Architecture

```
Input → [Validator] → [Log Parser] → [Router] → [Anomaly Detector] → [RAG Agent]
                                                                           ↓
                                                                   [Root Cause Agent]
                                                                           ↓
                                                                  [Confidence Checker]
                                                              ↙         ↓           ↘
                                                        score<90   score<85       score≥90
                                                      loop back   ask human      [Fix Agent]
                                                    (max 3 attempts) for context      ↓
                                                                                Final Report
                                                                                      ↓
                                                                               [SQLite Memory]
```

---

## The 8 Agents

| Agent | Responsibility |
|---|---|
| **Validator** | Rejects malformed input before any LLM call — saves cost, prevents downstream failures |
| **Log Parser** | Converts raw, messy log strings into structured data |
| **Router** | Classifies severity (CRITICAL / HIGH / LOW) and sets analysis depth |
| **Anomaly Detector** | Identifies failure patterns and generates an initial confidence score |
| **RAG Agent** | Searches 30 historical incidents via ChromaDB; falls back to DuckDuckGo if similarity < 0.6 |
| **Root Cause Analyzer** | Synthesizes all signals into a definitive root cause with confidence score |
| **Confidence Checker** | Decides: loop back to RAG, ask the human, or proceed to fix suggestions |
| **Fix Suggester** | Outputs immediate, short-term, and long-term remediation steps |

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Agent Orchestration | LangGraph with conditional edges | Handles cycles and branching — LangChain alone can't |
| LLM | Groq (Llama 3.3 70B) | Fast inference, free tier, good reasoning |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2) | 384-dim, fast, achieves 0.7+ similarity on incident data |
| Vector Store | ChromaDB | Lightweight, no infra required for this scale |
| Web Search | DuckDuckGo | No API key required, good for fallback |
| Persistent Memory | SQLite | Zero infra, cross-session history |
| Backend | FastAPI | Async, auto-generates OpenAPI docs |
| Frontend | Streamlit | Rapid iteration for ML interfaces |
| Deployment | Docker + HuggingFace Spaces + Streamlit Cloud | 24/7 uptime, no cold starts, free |

---

## Why all-MiniLM-L6-v2 for Embeddings

A common question. Larger models like `text-embedding-3-large` have better semantic accuracy but add API cost, latency, and an external dependency. For a system matching incident logs against 30 historical incidents, the tradeoff isn't worth it.

The key insight: chunk size matters more than model size for this use case. The 0.6 fallback threshold was determined empirically — below it, retrieved incidents came from different failure categories and actively misled the root cause agent, producing confident wrong answers. Getting this threshold right is what makes the web search fallback meaningful rather than decorative.

---

## Running Locally

**1. Clone and configure**
```bash
git clone https://github.com/ronnnie-cr7/ai-root-cause-analyzer
cd ai-root-cause-analyzer
cp .env.example .env
# Add your GROQ_API_KEY to .env
```

**2. Seed the vector database**
```bash
python -m rag.vectorstore
```

**3. Run with Docker**
```bash
docker-compose up --build
```

- API: http://localhost:8000/docs  
- Frontend: http://localhost:8501

---

## Demo

1. Open the [live frontend](https://ai-root-cause-analyzer.streamlit.app)
2. Click a sample log — Python exception, Nginx 502, or Kubernetes OOMKilled
3. Watch all 8 agents run with live status updates
4. If RAG similarity is low, see the agent switch to web search in real time
5. Download the full analysis report or check the Memory tab for past incidents

---

## Project Structure

```
ai-root-cause-analyzer/
├── agents/
│   ├── validator_agent.py       # Input guardrail — rejects before LLM calls
│   ├── log_parser_agent.py      # Structures raw logs
│   ├── router_agent.py          # Severity routing
│   ├── anomaly_agent.py         # Pattern detection + confidence scoring
│   ├── rag_agent.py             # ChromaDB retrieval + DuckDuckGo fallback
│   ├── root_cause_agent.py      # Root cause synthesis
│   ├── confidence_checker.py    # Loop / escalate / proceed decision
│   └── fix_agent.py             # Remediation suggestions
├── graph/
│   └── workflow.py              # LangGraph StateGraph with conditional edges
├── rag/
│   ├── vectorstore.py           # ChromaDB setup
│   ├── memory.py                # SQLite persistent memory
│   └── seed_incidents.py        # Seeds 30 historical incidents
├── api/main.py                  # FastAPI backend
├── frontend/app.py              # Streamlit UI
├── data/
│   ├── past_incidents.json      # 30 historical incidents
│   └── sample_logs/             # Sample log files
└── config/settings.py           # Configuration
```

---

## Future Improvements

- Parallel agent execution for faster analysis on CRITICAL severity
- Auto-add resolved incidents to ChromaDB so RAG improves over time
- Slack / PagerDuty integration for real-time alerting
- Fine-tune embeddings on real incident data for higher retrieval accuracy
- Multi-tenant support with per-team incident databases

---

## Author

**Ronit** — [GitHub](https://github.com/ronnnie-cr7) ·
