from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config.settings import GROQ_API_KEY, MODEL_NAME

llm = ChatGroq(api_key=GROQ_API_KEY, model_name=MODEL_NAME)

prompt = ChatPromptTemplate.from_template("""
You are a routing agent for an incident analysis system. 
Your job is to analyze parsed logs and decide the analysis strategy.

Parsed log data:
{parsed_logs}

Log type detected: {log_type}

Based on this, decide:
1. Severity routing (CRITICAL, HIGH, LOW)
   - CRITICAL: service down, OOM killed, CrashLoopBackOff, FATAL errors
   - HIGH: repeated errors, performance degradation, timeouts
   - LOW: warnings, single errors, minor issues

2. Analysis depth (DEEP, STANDARD)
   - DEEP: multiple error types, cascading failures, unknown root cause
   - STANDARD: single clear error type, known pattern

Respond in this exact format:
SEVERITY: <CRITICAL, HIGH, or LOW>
DEPTH: <DEEP or STANDARD>
ROUTING_REASON: <one sentence why>
FOCUS_AREAS: <comma separated list of what to focus on>
""")

def router_agent(state: dict) -> dict:
    print(">> Router Agent running...")

    chain = prompt | llm
    response = chain.invoke({
        "parsed_logs": state.get("parsed_logs", ""),
        "log_type": state.get("log_type", "unknown")
    })
    content = response.content

    severity_line = [l for l in content.split("\n") if "SEVERITY:" in l]
    severity = severity_line[0].replace("SEVERITY:", "").strip() if severity_line else "HIGH"

    depth_line = [l for l in content.split("\n") if "DEPTH:" in l]
    depth = depth_line[0].replace("DEPTH:", "").strip() if depth_line else "STANDARD"

    state["severity"] = severity
    state["analysis_depth"] = depth
    state["router_output"] = content
    state["loop_count"] = 0

    print(f">> Router: severity={severity}, depth={depth}")
    return state