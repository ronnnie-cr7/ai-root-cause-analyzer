from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from agents.validator_agent import validator_agent
from agents.log_parser_agent import log_parser_agent
from agents.router_agent import router_agent
from agents.anomaly_agent import anomaly_agent
from agents.rag_agent import rag_agent
from agents.root_cause_agent import root_cause_agent
from agents.fix_agent import fix_agent
from agents.confidence_checker import confidence_checker


class AgentState(TypedDict):
    raw_logs: str
    is_valid: bool
    validation_reason: str
    log_type: str
    parsed_logs: str
    severity: str
    analysis_depth: str
    router_output: str
    anomaly_report: str
    similar_incidents_raw: list
    rag_context: str
    root_cause: str
    fix_suggestions: str
    confidence_score: int
    needs_reanalysis: bool
    loop_count: int
    rag_source: str


def route_after_validation(state: dict) -> str:
    if state.get("is_valid"):
        return "valid"
    return "invalid"


def route_after_confidence(state: dict) -> str:
    if state.get("needs_reanalysis"):
        return "reanalyze"
    return "fix"


def invalid_input_handler(state: dict) -> dict:
    print(">> Invalid input detected — stopping pipeline")
    state["fix_suggestions"] = f"INVALID INPUT: {state.get('validation_reason', 'Input does not appear to be valid system logs. Please paste actual log files.')}"
    return state


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("validator", validator_agent)
    graph.add_node("invalid_handler", invalid_input_handler)
    graph.add_node("log_parser", log_parser_agent)
    graph.add_node("router", router_agent)
    graph.add_node("anomaly_detector", anomaly_agent)
    graph.add_node("rag_search", rag_agent)
    graph.add_node("root_cause_analyzer", root_cause_agent)
    graph.add_node("confidence_check", confidence_checker)
    graph.add_node("fix_suggester", fix_agent)

    graph.set_entry_point("validator")

    graph.add_conditional_edges(
        "validator",
        route_after_validation,
        {
            "valid": "log_parser",
            "invalid": "invalid_handler"
        }
    )

    graph.add_edge("invalid_handler", END)
    graph.add_edge("log_parser", "router")
    graph.add_edge("router", "anomaly_detector")
    graph.add_edge("anomaly_detector", "rag_search")
    graph.add_edge("rag_search", "root_cause_analyzer")
    graph.add_edge("root_cause_analyzer", "confidence_check")

    graph.add_conditional_edges(
        "confidence_check",
        route_after_confidence,
        {
            "reanalyze": "rag_search",
            "fix": "fix_suggester"
        }
    )

    graph.add_edge("fix_suggester", END)

    return graph.compile()


def run_analysis(raw_logs: str) -> dict:
    graph = build_graph()
    result = graph.invoke({"raw_logs": raw_logs})
    return result