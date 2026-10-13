import re

from orders import ORDERS


def classify_intent(state):
    query = state["query"].lower()

    if "cancel" in query:
        intent = "cancellation"
    elif "track" in query or "where" in query:
        intent = "tracking"
    elif "refund" in query:
            intent = "refund"
    elif re.search(r"\border\b|\bord\d+\b", query):
        intent = "details"
    else:
        intent = "unknown"

    return {"intent": intent}


def extract_order_id(state):
    match = re.search(r"\bORD\d+\b", state["query"], re.IGNORECASE)
    order_id = match.group(0).upper() if match else ""
    return {"order_id": order_id}


def _find_order(state):
    order_id = state["order_id"]
    order = ORDERS.get(order_id)
    if order is None:
        return None, {"response": f"Order {order_id} was not found."}
    return order, None


def tracking_node(state):
    order, error = _find_order(state)
    if error:
        return error
    return {"response": f"Order {state['order_id']} status: {order['status']}."}


def details_node(state):
    order, error = _find_order(state)
    if error:
        return error
    return {
        "response": (
            f"Order {state['order_id']}: {order['item']}, "
            f"status: {order['status']}, amount: ₹{order['amount']}."
        )
    }


def cancellation_node(state):
    order, error = _find_order(state)
    if error:
        return error
    if order["can_cancel"]:
        response = f"Order {state['order_id']} is eligible for cancellation."
    else:
        response = (
            f"Order {state['order_id']} cannot be cancelled because "
            f"its status is {order['status']}."
        )
    return {"response": response}


def refund_node(state):
    order, error = _find_order(state)
    if error:
        return error

    can_refund = order.get("can_refund")
    if can_refund is None:
        response = (
            f"Refund eligibility for order {state['order_id']} is not specified."
        )
        return {"response": response}
    elif can_refund:
        response = f"Order {state['order_id']} is eligible for a refund."
    else:
        response = (
            f"Order {state['order_id']} cannot be refunded because "
            f"its status is {order['status']}."
        )
    return {"response": response}

def route_request(state):
    if state["intent"] == "unknown" or not state["order_id"]:
        return "format_response"

    routes = {
        "tracking": "tracking",
        "details": "details",
        "cancellation": "cancellation",
        "refund": "refund",
    }
    return routes.get(state["intent"], "format_response")


def format_response(state):
    if state["intent"] == "unknown":
        response = "Please provide an order-related query so I can help."
    elif not state["order_id"]:
        response = "Please include an order ID, such as ORD101."
    else:
        response = state["response"]
        if not response:
            raise ValueError("The request handler did not provide a response.")
    return {"response": response}
