from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config.settings import GROQ_API_KEY, MODEL_NAME

llm = ChatGroq(api_key=GROQ_API_KEY, model_name=MODEL_NAME)

prompt = ChatPromptTemplate.from_template("""
You are an anomaly detection expert. Your only job is to find patterns and anomalies in parsed log data.

Analyze the following parsed log data and identify:
1. Severity level (CRITICAL / HIGH / MEDIUM / LOW)
2. Anomaly type (memory issue, network issue, crash, timeout, resource exhaustion, etc.)
3. Pattern detected (single event, repeated errors, cascading failure, gradual degradation)
4. Affected components
5. Timeline of events (what happened first, what followed)
6. Confidence score (0-100) that this is a real issue and not noise

Parsed Log Data:
{parsed_logs}

Respond in this exact format:
SEVERITY: <level>
ANOMALY TYPE: <type>
PATTERN: <pattern description>
AFFECTED COMPONENTS: <list>
TIMELINE: <step by step what happened>
CONFIDENCE: <score>/100
ANOMALY SUMMARY: <2 sentence summary of the anomaly detected>
""")

def anomaly_agent(state: dict) -> dict:
    print(">> Anomaly Detection Agent running...")

    parsed_logs = state.get("parsed_logs", "")

    if not parsed_logs:
        state["anomaly_report"] = "No parsed logs to analyze"
        return state

    chain = prompt | llm
    response = chain.invoke({"parsed_logs": parsed_logs})

    state["anomaly_report"] = response.content
    print(">> Anomaly Detection Agent done.")
    return state