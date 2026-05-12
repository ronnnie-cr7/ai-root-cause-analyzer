# 🔍 AI Root Cause Analyzer

A multi-agent AI system that automatically analyzes system logs, detects anomalies, 
matches against historical incidents, identifies root causes, and suggests actionable fixes.

Built with LangGraph, LangChain, Groq, ChromaDB, FastAPI, and Streamlit.

## 🌐 Live Demo

- **Frontend:** https://ai-root-cause-analyzer.streamlit.app
- **API Docs:** https://ai-root-cause-analyzer-mogq.onrender.com/docs

---

## 🏗️ Architecture

Raw Logs → [Log Parser Agent] → [Anomaly Detection Agent] → [RAG Agent] → [Root Cause Agent] → [Fix Suggestion Agent] → Final Report

Each agent is a specialized node in a LangGraph workflow. Agents pass context 
to each other through shared state — no agent does more than one job.

---

## 🤖 Agents

| Agent | Job |
|---|---|
| Log Parser | Structures raw messy logs into clean data |
| Anomaly Detector | Finds patterns, severity, and confidence score |
| RAG Agent | Searches ChromaDB for similar past incidents |
| Root Cause Analyzer | Synthesizes everything into a definitive root cause |
| Fix Suggester | Provides immediate, short term, and long term fixes |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Multi-Agent Orchestration | LangGraph |
| LLM + RAG | LangChain + Groq (Llama 3.3 70B) |
| Vector Memory | ChromaDB |
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

1. Paste or upload a log file into the Streamlit UI
2. Watch all 5 agents run in sequence
3. System outputs root cause, matched past incident, and fix suggestions with confidence scores

---

## 📁 Project Structure

```
ai-root-cause-analyzer/
├── agents/          # One file per agent, one job per agent
├── graph/           # LangGraph workflow connecting all agents
├── rag/             # ChromaDB setup and past incidents seeding
├── api/             # FastAPI backend
├── frontend/        # Streamlit UI
├── data/            # Sample logs and past incidents database
└── config/          # API keys and settings
```

---

## 💡 Key Design Decisions

- **Specialized agents over one big prompt** — each agent is an expert at one thing
- **RAG memory layer** — system learns from past incidents, not just current logs
- **Groq over OpenAI** — 10x faster inference, free tier, perfect for multi-agent chains
- **Confidence scores** — every output includes a confidence score so engineers can trust the result

---

## 🔮 Future Improvements

- Add PostgreSQL + Redis for production scale
- Slack/PagerDuty integration for real-time alerting
- Support for more log formats (AWS CloudWatch, Datadog)
- Fine-tune the LLM on real incident data
