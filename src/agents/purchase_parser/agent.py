from langgraph.graph import StateGraph, END
from .state import PurchaseState
from .nodes.parse_text.node import parse_text_node
from .nodes.calculate.node import calculate_node
from .nodes.build_response.node import build_response_node


def _route_after_parse(state: PurchaseState) -> str:
    if state.get("error"):
        return "error"
    return "calculate" if state.get("parsed_data", {}).get("items") else "build_response"


def _route_after_calculate(state: PurchaseState) -> str:
    return "error" if state.get("error") else "build_response"


def build_purchase_parser_graph():
    workflow = StateGraph(PurchaseState)

    workflow.add_node("parse_text", parse_text_node)
    workflow.add_node("calculate", calculate_node)
    workflow.add_node("build_response", build_response_node)

    workflow.set_entry_point("parse_text")

    workflow.add_conditional_edges("parse_text", _route_after_parse, {
        "calculate": "calculate",
        "build_response": "build_response",
        "error": END,
    })

    workflow.add_conditional_edges("calculate", _route_after_calculate, {
        "build_response": "build_response",
        "error": END,
    })

    workflow.add_edge("build_response", END)

    return workflow.compile()


agent = build_purchase_parser_graph()
