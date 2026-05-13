import streamlit as st
import requests
import os
import re

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

if "analysis_count" not in st.session_state:
    st.session_state.analysis_count = 0
if "anomaly_types" not in st.session_state:
    st.session_state.anomaly_types = []
if "confidence_scores" not in st.session_state:
    st.session_state.confidence_scores = []

st.title("🔍 AI Root Cause Analyzer")
st.caption("Agentic AI system that validates, routes, and analyzes logs with confidence-based decision making")

if st.session_state.analysis_count > 0:
    st.divider()
    st.subheader("📊 Session Dashboard")
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Analyses Run", st.session_state.analysis_count)
    d2.metric("Avg Confidence", f"{int(sum(st.session_state.confidence_scores) / len(st.session_state.confidence_scores))}%" if st.session_state.confidence_scores else "N/A")
    d3.metric("Last Anomaly Type", st.session_state.anomaly_types[-1] if st.session_state.anomaly_types else "N/A")
    d4.metric("Total Loops", sum(st.session_state.get("loop_counts", [0])))

st.divider()

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
        st.subheader("⚙️ Agents Running...")
        step0 = st.status("🛡️ Validator Agent — Checking input", expanded=False)
        step1 = st.status("📋 Log Parser Agent", expanded=False)
        step1b = st.status("🔀 Router Agent — Deciding strategy", expanded=False)
        step2 = st.status("⚠️ Anomaly Detection Agent", expanded=False)
        step3 = st.status("🕰️ RAG Agent — Searching past incidents", expanded=False)
        step4 = st.status("🎯 Root Cause Agent", expanded=False)
        step4b = st.status("🔍 Confidence Checker", expanded=False)
        step5 = st.status("🛠️ Fix Suggestion Agent", expanded=False)

        step0.update(state="running")

        try:
            response = requests.post(
                f"{API_URL}/analyze",
                json={"logs": logs}
            )
            result = response.json()

            if not result.get("is_valid"):
                step0.update(state="error")
                st.error(f"❌ Invalid Input: {result.get('validation_reason', 'Input does not appear to be valid system logs.')}")
            else:
                step0.update(state="complete")
                step1.update(state="complete")
                step1b.update(state="complete")
                step2.update(state="complete")
                step3.update(state="complete")
                step4.update(state="complete")
                step4b.update(state="complete")
                step5.update(state="complete")

                st.session_state.analysis_count += 1
                if "loop_counts" not in st.session_state:
                    st.session_state.loop_counts = []
                st.session_state.loop_counts.append(result.get("loop_count", 1))

                anomaly_line = [l for l in result["anomaly_report"].split("\n") if "ANOMALY TYPE:" in l]
                if anomaly_line:
                    st.session_state.anomaly_types.append(anomaly_line[0].replace("ANOMALY TYPE:", "").strip())
                rc_conf = re.search(r'CONFIDENCE:\s*(\d+)/100', result.get("root_cause", ""))
                if rc_conf:
                    st.session_state.confidence_scores.append(int(rc_conf.group(1)))

                severity = result.get("severity", "UNKNOWN")
                if severity == "CRITICAL":
                    st.error(f"🚨 Severity: {severity}")
                elif severity == "HIGH":
                    st.warning(f"⚠️ Severity: {severity}")
                else:
                    st.info(f"ℹ️ Severity: {severity}")

                c1, c2, c3 = st.columns(3)
                c1.metric("Log Type", result.get("log_type", "unknown").upper())
                c2.metric("Confidence Score", f"{result.get('confidence_score', 0)}/100")
                c3.metric("Analysis Loops", result.get("loop_count", 1))

                st.divider()

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("📋 Parsed Logs")
                    st.code(result["parsed_logs"], language="text")

                    st.subheader("⚠️ Anomaly Report")
                    anomaly_text = result["anomaly_report"]
                    confidence_match = re.search(r'CONFIDENCE:\s*(\d+)/100', anomaly_text)
                    if confidence_match:
                        confidence = int(confidence_match.group(1))
                        st.metric("Anomaly Confidence", f"{confidence}/100")
                        st.progress(confidence / 100)
                    st.code(anomaly_text, language="text")

                with col2:
                    st.subheader("🕰️ Similar Past Incidents")
                    if result["similar_incidents"]:
                        for inc in result["similar_incidents"]:
                            with st.expander(f"{inc['id']} — {inc['title']} (score: {inc['similarity_score']})"):
                                st.write(f"**Date:** {inc['date']}")
                                st.write(f"**Root Cause:** {inc['root_cause']}")
                                st.write(f"**Fix Applied:** {inc['fix']}")

                    st.subheader("🔗 RAG Context")
                    rag_source = result.get("rag_source", "chromadb")
                    if rag_source == "web_search":
                        st.warning("⚠️ RAG score too low — agent searched the web for similar incidents")
                    else:
                        st.success("✅ Match found in internal incident database")
                    st.code(result["rag_context"], language="text")

                st.divider()

                st.subheader("🎯 Root Cause")
                root_cause_text = result["root_cause"]
                rc_confidence_match = re.search(r'CONFIDENCE:\s*(\d+)/100', root_cause_text)
                if rc_confidence_match:
                    rc_confidence = int(rc_confidence_match.group(1))
                    st.metric("Root Cause Confidence", f"{rc_confidence}/100")
                    st.progress(rc_confidence / 100)
                st.code(root_cause_text, language="text")

                st.subheader("🛠️ Fix Suggestions")
                st.code(result["fix_suggestions"], language="text")

                st.divider()

                full_report = f"""
AI ROOT CAUSE ANALYZER — FULL REPORT
Generated by AI Root Cause Analyzer
=====================================

LOG TYPE: {result.get("log_type", "unknown").upper()}
SEVERITY: {result.get("severity", "unknown")}
CONFIDENCE SCORE: {result.get("confidence_score", 0)}/100
ANALYSIS LOOPS: {result.get("loop_count", 1)}

PARSED LOGS
-----------
{result["parsed_logs"]}

ANOMALY REPORT
--------------
{result["anomaly_report"]}

SIMILAR PAST INCIDENTS
----------------------
"""
                for inc in result["similar_incidents"]:
                    full_report += f"""
{inc["id"]} — {inc["title"]} (similarity: {inc["similarity_score"]})
Date: {inc["date"]}
Root Cause: {inc["root_cause"]}
Fix: {inc["fix"]}
"""
                full_report += f"""
RAG CONTEXT
-----------
{result["rag_context"]}

ROOT CAUSE
----------
{result["root_cause"]}

FIX SUGGESTIONS
---------------
{result["fix_suggestions"]}
"""

                st.download_button(
                    label="📥 Download Full Report",
                    data=full_report,
                    file_name="root_cause_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        except Exception as e:
            step0.update(state="error")
            st.error(f"Error connecting to API: {e}")