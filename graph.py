

from langgraph.graph import StateGraph, START, END
from state import orderstate
from nodes import (
    cancellation_node,
    classify_intent,
    details_node,
    extract_order_id,
    format_response,
    route_request,
    tracking_node,
)


def build_graph():
    builder = StateGraph(orderstate)

    builder.add_node("classify_intent", classify_intent)
    builder.add_node("extract_order_id", extract_order_id)
    builder.add_node("tracking", tracking_node)
    builder.add_node("details", details_node)
    builder.add_node("cancellation", cancellation_node)
    builder.add_node("format_response", format_response)

    builder.add_edge(START, "classify_intent")
    builder.add_edge("classify_intent", "extract_order_id")
    builder.add_conditional_edges(
        "extract_order_id",
        route_request,
        {
            "tracking": "tracking",
            "details": "details",
            "cancellation": "cancellation",
            "format_response": "format_response",
        },
    )
    builder.add_edge("tracking", "format_response")
    builder.add_edge("details", "format_response")
    builder.add_edge("cancellation", "format_response")
    builder.add_edge("format_response", END)

    return builder.compile()