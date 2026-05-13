from graph.workflow import run_analysis

print("TEST 1 — Valid logs")
result = run_analysis(open("data/sample_logs/python_error.log").read())
print(f"Valid: {result.get('is_valid')}")
print(f"Severity: {result.get('severity')}")
print(f"Confidence: {result.get('confidence_score')}")
print(f"Loops: {result.get('loop_count')}")
print(f"Root Cause: {result.get('root_cause', '')[:200]}")

print("\nTEST 2 — Invalid input")
result2 = run_analysis("hello my name is ronit and i like cricket")
print(f"Valid: {result2.get('is_valid')}")
print(f"Response: {result2.get('fix_suggestions')}")