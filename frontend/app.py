import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="AI Root Cause Analyzer",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AI Root Cause Analyzer")
st.caption("Multi-agent system that analyzes logs and identifies root causes automatically")

st.divider()

input_method = st.radio("Input Method", ["Paste Logs", "Upload Log File"], horizontal=True)

logs = None

if input_method == "Paste Logs":
    logs = st.text_area("Paste your logs here", height=200, placeholder="Paste raw logs...")
else:
    uploaded_file = st.file_uploader("Upload a log file", type=["log", "txt"])
    if uploaded_file:
        logs = uploaded_file.read().decode("utf-8")
        st.code(logs, language="text")

st.divider()

if st.button("🚀 Analyze Logs", type="primary", use_container_width=True):
    if not logs or logs.strip() == "":
        st.error("Please provide logs first.")
    else:
        with st.spinner("Agents are analyzing your logs..."):
            try:
                response = requests.post(
                    f"{API_URL}/analyze",
                    json={"logs": logs}
                )
                result = response.json()

                st.success("Analysis complete!")
                st.divider()

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("📋 Parsed Logs")
                    st.code(result["parsed_logs"], language="text")

                    st.subheader("⚠️ Anomaly Report")
                    st.code(result["anomaly_report"], language="text")

                with col2:
                    st.subheader("🕰️ Similar Past Incidents")
                    if result["similar_incidents"]:
                        for inc in result["similar_incidents"]:
                            with st.expander(f"{inc['id']} — {inc['title']} (score: {inc['similarity_score']})"):
                                st.write(f"**Date:** {inc['date']}")
                                st.write(f"**Root Cause:** {inc['root_cause']}")
                                st.write(f"**Fix Applied:** {inc['fix']}")
                    
                    st.subheader("🔗 RAG Context")
                    st.code(result["rag_context"], language="text")

                st.divider()

                st.subheader("🎯 Root Cause")
                st.code(result["root_cause"], language="text")

                st.subheader("🛠️ Fix Suggestions")
                st.code(result["fix_suggestions"], language="text")

            except Exception as e:
                st.error(f"Error connecting to API: {e}")