from langgraph.graph import StateGraph, END
from typing import TypedDict
from agents.log_parser_agent import log_parser_agent
from agents.anomaly_agent import anomaly_agent
from agents.rag_agent import rag_agent
from agents.root_cause_agent import root_cause_agent
from agents.fix_agent import fix_agent


class AgentState(TypedDict):
    raw_logs: str
    parsed_logs: str
    anomaly_report: str
    similar_incidents_raw: list
    rag_context: str
    root_cause: str
    fix_suggestions: str


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("log_parser", log_parser_agent)
    graph.add_node("anomaly_detector", anomaly_agent)
    graph.add_node("rag_search", rag_agent)
    graph.add_node("root_cause_analyzer", root_cause_agent)
    graph.add_node("fix_suggester", fix_agent)

    graph.set_entry_point("log_parser")
    graph.add_edge("log_parser", "anomaly_detector")
    graph.add_edge("anomaly_detector", "rag_search")
    graph.add_edge("rag_search", "root_cause_analyzer")
    graph.add_edge("root_cause_analyzer", "fix_suggester")
    graph.add_edge("fix_suggester", END)

    return graph.compile()


def run_analysis(raw_logs: str) -> dict:
    graph = build_graph()
    result = graph.invoke({"raw_logs": raw_logs})
    return result