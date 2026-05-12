from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config.settings import GROQ_API_KEY, MODEL_NAME

llm = ChatGroq(api_key=GROQ_API_KEY, model_name=MODEL_NAME)

prompt = ChatPromptTemplate.from_template("""
You are a senior site reliability engineer with 15 years of experience.
Your job is to synthesize all available information and identify the definitive root cause.

You have been given:

1. PARSED LOG DATA:
{parsed_logs}

2. ANOMALY REPORT:
{anomaly_report}

3. HISTORICAL CONTEXT FROM PAST INCIDENTS:
{rag_context}

Using ALL of this information together, identify:
1. The single most likely root cause
2. Why you believe this is the root cause (reasoning)
3. Contributing factors that made it worse
4. What triggered it (the initial event)
5. Confidence level (0-100)

Respond in this exact format:
ROOT CAUSE: <one clear sentence stating the root cause>
REASONING: <step by step explanation of how you reached this conclusion>
CONTRIBUTING FACTORS: <list of things that made it worse>
TRIGGER EVENT: <what initially caused this>
CONFIDENCE: <score>/100
IMPACT ASSESSMENT: <what systems/users are affected and how severely>
""")

def root_cause_agent(state: dict) -> dict:
    print(">> Root Cause Agent running...")

    chain = prompt | llm
    response = chain.invoke({
        "parsed_logs": state.get("parsed_logs", ""),
        "anomaly_report": state.get("anomaly_report", ""),
        "rag_context": state.get("rag_context", "")
    })

    state["root_cause"] = response.content
    print(">> Root Cause Agent done.")
    return state