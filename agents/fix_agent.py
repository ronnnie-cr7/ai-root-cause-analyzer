from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config.settings import GROQ_API_KEY, MODEL_NAME

llm = ChatGroq(api_key=GROQ_API_KEY, model_name=MODEL_NAME)

prompt = ChatPromptTemplate.from_template("""
You are a senior DevOps engineer. Your job is to suggest specific, actionable fixes.

You have been given:

1. ROOT CAUSE IDENTIFIED:
{root_cause}

2. HISTORICAL FIXES THAT WORKED BEFORE:
{rag_context}

Based on this, provide fixes in order of priority:
1. Immediate fix (do this right now to stop the bleeding)
2. Short term fix (do this within 24 hours)
3. Long term fix (do this within a week to prevent recurrence)
4. Monitoring to add (so this never goes undetected again)

Respond in this exact format:
IMMEDIATE FIX: <what to do right now, specific commands or steps>
SHORT TERM FIX: <what to do within 24 hours>
LONG TERM FIX: <what to do within a week>
MONITORING TO ADD: <specific alerts or metrics to track>
ESTIMATED RECOVERY TIME: <how long until system is fully healthy>
PREVENTION SUMMARY: <one paragraph on how to prevent this permanently>
""")

def fix_agent(state: dict) -> dict:
    print(">> Fix Suggestion Agent running...")

    chain = prompt | llm
    response = chain.invoke({
        "root_cause": state.get("root_cause", ""),
        "rag_context": state.get("rag_context", "")
    })

    state["fix_suggestions"] = response.content
    print(">> Fix Suggestion Agent done.")
    return state