from graph.workflow import run_analysis

raw_logs = open("data/sample_logs/python_error.log").read()

print("Starting full analysis pipeline...\n")
result = run_analysis(raw_logs)

print("\n========== FINAL REPORT ==========")
print("\n--- PARSED LOGS ---")
print(result["parsed_logs"])

print("\n--- ANOMALY REPORT ---")
print(result["anomaly_report"])

print("\n--- RAG CONTEXT ---")
print(result["rag_context"])

print("\n--- ROOT CAUSE ---")
print(result["root_cause"])

print("\n--- FIX SUGGESTIONS ---")
print(result["fix_suggestions"])