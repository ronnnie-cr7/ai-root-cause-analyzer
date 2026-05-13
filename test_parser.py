from graph.workflow import run_analysis

print("TEST — Human in the loop trigger")
ambiguous_log = """
2025-09-18 10:00:01 WARN service-x - response time degraded
2025-09-18 10:00:02 WARN service-x - something seems off
2025-09-18 10:00:03 WARN service-x - performance not normal
"""

result = run_analysis(ambiguous_log)
print(f"Needs human input: {result.get('needs_human_input')}")
print(f"Confidence: {result.get('confidence_score')}")
print(f"Loop count: {result.get('loop_count')}")
print(f"Fix suggestions preview: {result.get('fix_suggestions', '')[:100]}")