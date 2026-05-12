from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from rag.vectorstore import search_similar_incidents
from config.settings import GROQ_API_KEY, MODEL_NAME

llm = ChatGroq(api_key=GROQ_API_KEY, model_name=MODEL_NAME)

prompt = ChatPromptTemplate.from_template("""
You are a historical incident analyst. Your job is to analyze similar past incidents and extract useful patterns.

Current anomaly detected:
{anomaly_report}

Similar past incidents found:
{similar_incidents}

Based on these past incidents, provide:
1. Which past incident is most relevant and why
2. What the common pattern is between past and current
3. What fixes worked before that might apply now
4. Any warnings based on how past incidents escalated

Respond in this exact format:
MOST RELEVANT INCIDENT: <incident ID and title>
SIMILARITY REASON: <why it matches>
COMMON PATTERN: <what pattern repeats>
HISTORICAL FIXES THAT APPLY: <list fixes from past incidents>
ESCALATION WARNING: <how this could get worse based on past incidents>
""")

def rag_agent(state: dict) -> dict:
    print(">> RAG Agent running...")

    anomaly_report = state.get("anomaly_report", "")

    if not anomaly_report:
        state["rag_context"] = "No anomaly report to search against"
        return state

    # Build search query from anomaly report
    search_query = anomaly_report[:500]

    similar = search_similar_incidents(search_query, n_results=3)

    # Format for the prompt
    formatted_incidents = ""
    for inc in similar:
        formatted_incidents += f"""
---
ID: {inc['id']}
Title: {inc['title']}
Date: {inc['date']}
Root Cause: {inc['root_cause']}
Fix Applied: {inc['fix']}
Similarity Score: {inc['similarity_score']}
---
"""

    state["similar_incidents_raw"] = similar

    chain = prompt | llm
    response = chain.invoke({
        "anomaly_report": anomaly_report,
        "similar_incidents": formatted_incidents
    })

    state["rag_context"] = response.content
    print(">> RAG Agent done.")
    return state