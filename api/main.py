from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from graph.workflow import run_analysis
from rag.memory import save_analysis, get_recent_analyses, get_stats
import uvicorn

app = FastAPI(title="AI Root Cause Analyzer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class LogInput(BaseModel):
    logs: str

@app.get("/")
def root():
    return {"status": "running", "message": "AI Root Cause Analyzer is live"}

@app.post("/analyze")
async def analyze_logs(input: LogInput):
    result = run_analysis(input.logs)
    if result.get("is_valid") and result.get("fix_suggestions") != "NEEDS_HUMAN_INPUT":
        save_analysis(result, input.logs)
    return {
        "is_valid": result.get("is_valid"),
        "validation_reason": result.get("validation_reason"),
        "severity": result.get("severity"),
        "log_type": result.get("log_type"),
        "parsed_logs": result.get("parsed_logs"),
        "anomaly_report": result.get("anomaly_report"),
        "rag_context": result.get("rag_context"),
        "root_cause": result.get("root_cause"),
        "fix_suggestions": result.get("fix_suggestions"),
        "similar_incidents": result.get("similar_incidents_raw", []),
        "confidence_score": result.get("confidence_score"),
        "loop_count": result.get("loop_count"),
        "rag_source": result.get("rag_source")
    }

@app.post("/analyze/file")
async def analyze_file(file: UploadFile = File(...)):
    content = await file.read()
    logs = content.decode("utf-8")
    result = run_analysis(logs)
    if result.get("is_valid") and result.get("fix_suggestions") != "NEEDS_HUMAN_INPUT":
        save_analysis(result, logs)
    return {
        "filename": file.filename,
        "is_valid": result.get("is_valid"),
        "validation_reason": result.get("validation_reason"),
        "severity": result.get("severity"),
        "log_type": result.get("log_type"),
        "parsed_logs": result.get("parsed_logs"),
        "anomaly_report": result.get("anomaly_report"),
        "rag_context": result.get("rag_context"),
        "root_cause": result.get("root_cause"),
        "fix_suggestions": result.get("fix_suggestions"),
        "similar_incidents": result.get("similar_incidents_raw", []),
        "confidence_score": result.get("confidence_score"),
        "loop_count": result.get("loop_count"),
        "rag_source": result.get("rag_source")
    }

@app.get("/memory")
def get_memory():
    return {
        "recent_analyses": get_recent_analyses(5),
        "stats": get_stats()
    }

@app.post("/reanalyze")
async def reanalyze_logs(input: LogInput):
    result = run_analysis(input.logs)
    if result.get("is_valid"):
        save_analysis(result, input.logs)
    return {
        "is_valid": result.get("is_valid"),
        "validation_reason": result.get("validation_reason"),
        "severity": result.get("severity"),
        "log_type": result.get("log_type"),
        "parsed_logs": result.get("parsed_logs"),
        "anomaly_report": result.get("anomaly_report"),
        "rag_context": result.get("rag_context"),
        "root_cause": result.get("root_cause"),
        "fix_suggestions": result.get("fix_suggestions") if result.get("fix_suggestions") != "NEEDS_HUMAN_INPUT" else "Based on the context provided, further manual investigation is recommended. Check recent deployments, config changes, and resource utilization.",
        "similar_incidents": result.get("similar_incidents_raw", []),
        "confidence_score": result.get("confidence_score"),
        "loop_count": result.get("loop_count"),
        "rag_source": result.get("rag_source")
    }

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)