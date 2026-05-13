# 🔍 AI Root Cause Analyzer

A production-grade agentic AI system that validates, routes, and analyzes system logs using a multi-agent LangGraph architecture with confidence-based decision making.

Built with LangGraph, LangChain, Groq, ChromaDB, FastAPI, and Streamlit.

## 🌐 Live Demo

- **Frontend:** https://ai-root-cause-analyzer.streamlit.app
- **API Docs:** https://ai-root-cause-analyzer-mogq.onrender.com/docs

---

## 🏗️ Agentic Architecture

```
Input → [Validator] → [Log Parser] → [Router] → [Anomaly Detector] → [RAG Agent]
                                                                           ↓
                                                                   [Root Cause Agent]
                                                                           ↓
                                                                  [Confidence Checker]
                                                                    ↙           ↘
                                                            score < 80      score ≥ 80
                                                          loop back to       [Fix Agent]
                                                           RAG Agent             ↓
                                                          (max 3 loops)      Final Report
```

This is a true agentic system — not a fixed pipeline. The agent:
- **Validates** input before wasting API calls
- **Routes** based on severity (CRITICAL / HIGH / LOW)
- **Loops back** if confidence is too low
- **Stops early** on invalid input

---

## 🤖 Agents

| Agent | Job |
|---|---|
| Validator | Checks if input is actually valid system logs |
| Log Parser | Structures raw messy logs into clean data |
| Router | Decides severity and analysis depth |
| Anomaly Detector | Finds patterns, severity, and confidence score |
| RAG Agent | Searches ChromaDB for similar past incidents |
| Root Cause Analyzer | Synthesizes everything into a definitive root cause |
| Confidence Checker | Decides to loop back or proceed based on confidence |
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
| Backend API | FastAPI |
| Frontend | Streamlit |
| Deployment | Docker + Docker Compose |

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

---

## 📸 Demo Flow

1. Click a sample log button (Python, Nginx, or Kubernetes)
2. Watch 8 agents run with live status updates
3. System validates input, routes by severity, analyzes with confidence scoring
4. If confidence is low the system automatically loops back for deeper analysis
5. Download the full report as a text file

---

## ✨ Features

- **Input validation** — rejects garbage input before wasting API calls
- **Severity routing** — CRITICAL / HIGH / LOW with visual badges
- **Confidence loop** — automatically re-analyzes if confidence below 80%
- **3 sample log types** — Python errors, Nginx 502s, Kubernetes CrashLoops
- **Semantic RAG** — SentenceTransformer embeddings, 0.7+ similarity scores
- **Session dashboard** — tracks analyses run, avg confidence, total loops
- **Download report** — export full analysis as a text file
- **Docker deployment** — entire stack runs with one command

---

## 📁 Project Structure

```
ai-root-cause-analyzer/
├── agents/          # One file per agent, one job per agent
│   ├── validator_agent.py
│   ├── log_parser_agent.py
│   ├── router_agent.py
│   ├── anomaly_agent.py
│   ├── rag_agent.py
│   ├── root_cause_agent.py
│   ├── confidence_checker.py
│   └── fix_agent.py
├── graph/           # LangGraph workflow with conditional edges
├── rag/             # ChromaDB setup and past incidents seeding
├── api/             # FastAPI backend
├── frontend/        # Streamlit UI
├── data/            # Sample logs and past incidents database
└── config/          # API keys and settings
```

---

## 💡 Key Design Decisions

- **True agentic over fixed pipeline** — conditional edges and confidence loops make this a genuine agent, not just a sequential chain
- **Validator guardrail** — invalid input is rejected before any LLM calls, saving tokens and API quota
- **Severity-based routing** — CRITICAL incidents get DEEP analysis, LOW severity gets STANDARD
- **SentenceTransformer embeddings** — 0.7+ similarity vs 0.1 with default embeddings
- **Max loop limit** — agent loops max 3 times to prevent infinite recursion

---

## 🔮 Future Improvements

- Human in the loop — agent asks for clarification when stuck
- Web search tool fallback when RAG finds no matches
- Memory across sessions using PostgreSQL
- Slack/PagerDuty integration for real-time alerting
- Fine-tune on real incident data