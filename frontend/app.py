import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

SAMPLE_LOG = """2025-09-15 14:23:01 ERROR payment-service - Traceback (most recent call last):
2025-09-15 14:23:01 ERROR payment-service -   File "handler.py", line 87, in process_transaction
2025-09-15 14:23:01 ERROR payment-service - MemoryError: unable to allocate memory
2025-09-15 14:23:02 ERROR payment-service - OOM killer activated on process 4421
2025-09-15 14:23:02 WARN  payment-service - Heap usage at 98%, threshold exceeded
2025-09-15 14:23:03 ERROR payment-service - Connection pool exhausted: max 20 connections reached
2025-09-15 14:23:05 FATAL payment-service - Service shutting down unexpectedly"""

SAMPLE_NGINX = """2025-09-16 09:12:01 [error] upstream timed out (110: Connection timed out) while reading response header from upstream
2025-09-16 09:12:01 [error] *1234 connect() failed (111: Connection refused) while connecting to upstream
2025-09-16 09:12:02 [error] 502 Bad Gateway - upstream: fastapi-service:8000
2025-09-16 09:12:03 [warn] 10240 worker_connections are not enough
2025-09-16 09:12:05 [error] *1235 upstream timed out (110: Connection timed out)
2025-09-16 09:12:06 [error] 502 Bad Gateway - upstream: fastapi-service:8000
2025-09-16 09:12:08 [error] *1236 no live upstreams while connecting to upstream"""

SAMPLE_KUBERNETES = """2025-09-17 11:45:01 WARNING pod/payment-service-7d9f8b-xkq2p - OOMKilled: container exceeded memory limit
2025-09-17 11:45:02 WARNING pod/payment-service-7d9f8b-xkq2p - Back-off restarting failed container
2025-09-17 11:45:03 ERROR pod/payment-service-7d9f8b-xkq2p - Liveness probe failed: HTTP probe failed with statuscode: 503
2025-09-17 11:45:04 WARNING node/worker-node-1 - Evicting pod due to memory pressure
2025-09-17 11:45:05 ERROR pod/payment-service-7d9f8b-xkq2p - CrashLoopBackOff: restarting container
2025-09-17 11:45:10 WARNING node/worker-node-1 - Memory usage at 95%, threshold exceeded"""

st.set_page_config(
    page_title="AI Root Cause Analyzer",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AI Root Cause Analyzer")
st.caption("Multi-agent system that analyzes logs and identifies root causes automatically")

st.divider()

# Sample log buttons
st.write("**Quick Load Sample Logs:**")
col1, col2, col3 = st.columns(3)

if col1.button("🐍 Python Error", use_container_width=True):
    st.session_state.sample_log = SAMPLE_LOG

if col2.button("🌐 Nginx 502 Error", use_container_width=True):
    st.session_state.sample_log = SAMPLE_NGINX

if col3.button("☸️ Kubernetes CrashLoop", use_container_width=True):
    st.session_state.sample_log = SAMPLE_KUBERNETES

st.divider()

input_method = st.radio("Input Method", ["Paste Logs", "Upload Log File"], horizontal=True)

logs = None

if input_method == "Paste Logs":
    default = st.session_state.get("sample_log", "")
    logs = st.text_area("Paste your logs here", value=default, height=200, placeholder="Paste raw logs or click a sample above...")
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
        # Live agent steps
        st.subheader("⚙️ Agents Running...")
        step1 = st.status("📋 Log Parser Agent", expanded=False)
        step2 = st.status("⚠️ Anomaly Detection Agent", expanded=False)
        step3 = st.status("🕰️ RAG Agent — Searching past incidents", expanded=False)
        step4 = st.status("🎯 Root Cause Agent", expanded=False)
        step5 = st.status("🛠️ Fix Suggestion Agent", expanded=False)

        step1.update(state="running")

        try:
            response = requests.post(
                f"{API_URL}/analyze",
                json={"logs": logs}
            )
            result = response.json()

            step1.update(state="complete")
            step2.update(state="complete")
            step3.update(state="complete")
            step4.update(state="complete")
            step5.update(state="complete")

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
            step1.update(state="error")
            st.error(f"Error connecting to API: {e}")