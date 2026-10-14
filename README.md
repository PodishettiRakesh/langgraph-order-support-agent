# LangGraph Order Support Agent

A simple order support assistant built with Python and LangGraph. It classifies user requests, extracts an order ID, routes the request to the correct handler, and returns a response using mock order data.

## Current implementation

- Rule-based intent detection (`cancel`, `track`, `refund`, or order detail lookup)
- Order ID extraction from queries like `ORD101`
- Conditional routing through a LangGraph workflow
- Mock order data for tracking, detail checks, cancellation, and refund eligibility
- CLI interaction via `main.py`

## Project structure

```text
order_support_agent/
├── README.md
├── graph.py          # Builds and compiles the LangGraph workflow
├── main.py           # CLI entry point for user interaction
├── nodes.py          # Intent detection, order lookup, routing, and response logic
├── orders.py         # Sample order dataset used by the agent
├── state.py          # Typed state for the workflow
├── llm.py            # OpenRouter/ChatOpenAI test setup (optional LLM integration)
└── .env              # Optional environment variables for API keys
```

## How it works

The app starts in `main.py`, creates the graph from `graph.py`, and runs a loop that accepts customer queries. Each request flows through the state graph:

1. classify the user intent
2. extract the order ID
3. route to the relevant node
4. retrieve order info or check eligibility
5. return the final response

## Run it

```bash
python main.py
```

Example inputs:
- `Track order ORD102`
- `Cancel order ORD101`
- `Check order ORD103`
- `Refund for ORD104`

## Brief note

This is a lightweight demo project for learning LangGraph patterns and order-support workflows. It uses mock data rather than a real backend or database.
