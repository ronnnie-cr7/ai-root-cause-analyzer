from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config.settings import GROQ_API_KEY, MODEL_NAME

llm = ChatGroq(api_key=GROQ_API_KEY, model_name=MODEL_NAME)

prompt = ChatPromptTemplate.from_template("""
You are a log parsing expert. Your only job is to extract structured information from raw logs.

Analyze the following raw log input and extract:
1. Log type (nginx, python, kubernetes, docker, or unknown)
2. Error messages found
3. Timestamps of errors (if present)
4. Service or component names mentioned
5. Error codes or status codes
6. Any keywords that indicate the problem (OOM, timeout, crash, 502, etc.)

Raw Logs:
{raw_logs}

Respond in this exact format:
LOG TYPE: <type>
ERRORS FOUND: <list each error on a new line>
TIMESTAMPS: <list timestamps or "not found">
SERVICES: <list service/component names>
ERROR CODES: <list codes or "none">
KEYWORDS: <comma separated keywords>
SUMMARY: <one sentence summary of what these logs show>
""")

def log_parser_agent(state: dict) -> dict:
    print(">> Log Parser Agent running...")
    
    raw_logs = state.get("raw_logs", "")
    
    if not raw_logs:
        state["parsed_logs"] = "No logs provided"
        return state
    
    chain = prompt | llm
    response = chain.invoke({"raw_logs": raw_logs})
    
    state["parsed_logs"] = response.content
    print(">> Log Parser Agent done.")
    return state