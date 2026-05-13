from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config.settings import GROQ_API_KEY, MODEL_NAME

llm = ChatGroq(api_key=GROQ_API_KEY, model_name=MODEL_NAME)

prompt = ChatPromptTemplate.from_template("""
You are an input validator. Your only job is to determine if the input is a valid system log.

Valid logs contain things like:
- Timestamps (2025-01-01 12:00:00)
- Log levels (ERROR, WARN, INFO, DEBUG, FATAL, CRITICAL)
- Service or component names
- Error messages or stack traces
- HTTP status codes
- System events

Input to validate:
{raw_logs}

Respond in this exact format and nothing else:
IS_VALID: <YES or NO>
REASON: <one sentence explanation>
LOG_TYPE: <nginx, kubernetes, python, docker, unknown, or invalid>
""")

def validator_agent(state: dict) -> dict:
    print(">> Validator Agent running...")

    raw_logs = state.get("raw_logs", "")

    if not raw_logs or raw_logs.strip() == "":
        state["is_valid"] = False
        state["validation_reason"] = "No input provided"
        state["log_type"] = "invalid"
        return state

    chain = prompt | llm
    response = chain.invoke({"raw_logs": raw_logs})
    content = response.content

    is_valid = "IS_VALID: YES" in content
    
    reason_line = [l for l in content.split("\n") if "REASON:" in l]
    reason = reason_line[0].replace("REASON:", "").strip() if reason_line else "Unknown"

    log_type_line = [l for l in content.split("\n") if "LOG_TYPE:" in l]
    log_type = log_type_line[0].replace("LOG_TYPE:", "").strip() if log_type_line else "unknown"

    state["is_valid"] = is_valid
    state["validation_reason"] = reason
    state["log_type"] = log_type

    print(f">> Validator: valid={is_valid}, type={log_type}")
    return state