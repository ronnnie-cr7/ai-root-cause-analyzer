from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from rag.vectorstore import search_similar_incidents
from config.settings import GROQ_API_KEY, MODEL_NAME

llm = ChatGroq(api_key=GROQ_API_KEY, model_name=MODEL_NAME)
search_tool = DuckDuckGoSearchRun()

rag_prompt = ChatPromptTemplate.from_template("""
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

web_prompt = ChatPromptTemplate.from_template("""
You are a historical incident analyst. RAG search found no strong matches in the internal database.
You have been given web search results about similar incidents.

Current anomaly detected:
{anomaly_report}

Web search results:
{web_results}

Based on these web results, provide:
1. What similar incidents others have experienced
2. Common patterns found online
3. Fixes that have worked for others
4. Any warnings or escalation risks

Respond in this exact format:
MOST RELEVANT INCIDENT: Web search result — <brief title>
SIMILARITY REASON: <why web results match current issue>
COMMON PATTERN: <what pattern repeats across web results>
HISTORICAL FIXES THAT APPLY: <list fixes found online>
ESCALATION WARNING: <how this could get worse based on web results>
""")

def rag_agent(state: dict) -> dict:
    print(">> RAG Agent running...")

    anomaly_report = state.get("anomaly_report", "")

    if not anomaly_report:
        state["rag_context"] = "No anomaly report to search against"
        return state

    search_query = anomaly_report[:500]
    similar = search_similar_incidents(search_query, n_results=3)

    best_score = max([r["similarity_score"] for r in similar], default=0)
    print(f">> RAG best similarity score: {best_score}")

    if best_score >= 0.6:
        print(">> RAG score sufficient — using ChromaDB results")
        state["rag_source"] = "chromadb"

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

        chain = rag_prompt | llm
        response = chain.invoke({
            "anomaly_report": anomaly_report,
            "similar_incidents": formatted_incidents
        })

    else:
        print(">> RAG score too low — falling back to web search")
        state["rag_source"] = "web_search"
        state["similar_incidents_raw"] = similar

        keywords = ""
        for line in anomaly_report.split("\n"):
            if "KEYWORDS:" in line:
                keywords = line.replace("KEYWORDS:", "").strip()
                break

        search_query = f"production incident {keywords} root cause fix site:engineering.atspotify.com OR site:netflixtechblog.com OR site:engineering.linkedin.com OR stackoverflow.com"
        print(f">> Searching web for: {keywords}")

        try:
            web_results = search_tool.run(keywords + " production incident root cause fix")
        except Exception as e:
            web_results = f"Web search failed: {e}"
            print(f">> Web search error: {e}")

        chain = web_prompt | llm
        response = chain.invoke({
            "anomaly_report": anomaly_report,
            "web_results": web_results
        })

    state["rag_context"] = response.content
    print(">> RAG Agent done.")
    return state