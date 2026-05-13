from graph.workflow import run_analysis

print("TEST — Web search trigger")
obscure_log = """
2025-09-18 ERROR istio-proxy - upstream connect error or disconnect/reset before headers
2025-09-18 ERROR istio-proxy - envoy connection failure TLS handshake timeout
2025-09-18 ERROR service-mesh - circuit breaker open percentage 100
"""
result = run_analysis(obscure_log)
print(f"RAG Source: {result.get('rag_source')}")