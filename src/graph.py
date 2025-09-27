from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import (
    initialize_agent_state,
    parse_pdf,
    plan_summary,
    summarize,
    finish_node,
)
from utils import count_tokens


def should_plan_summary(state):
    """Conditional routing function - plan summary if token count > 3000"""
    token_count = state.get("token_count", 0)
    if token_count > 3000:
        return "plan_summary"
    else:
        return "end"


def build_graph():
    workflow = StateGraph(AgentState)

    # --- End entry point ---
    workflow.set_entry_point("initialize")

    # --- Add nodes ---
    workflow.add_node("initialize", initialize_agent_state)
    workflow.add_node("parse_pdf", parse_pdf)
    workflow.add_node("summarizer", summarize)
    workflow.add_node("count_tokens", count_tokens)
    workflow.add_node("plan_summary", plan_summary)
    workflow.add_node("finish", finish_node)

    # --- Add edges ---
    workflow.add_edge("initialize", "parse_pdf")  # first initialize the agent state
    workflow.add_edge("parse_pdf", "count_tokens")  # after parsing, count tokens

    workflow.add_conditional_edges(
        "count_tokens",
        should_plan_summary,
        {
            "plan_summary": "plan_summary",
            "end": END,
        },
    )

    workflow.add_edge("plan_summary", "summarizer")  # after planning, summarize
    workflow.add_edge("summarizer", END)
    workflow.add_edge("finish", END)

    return workflow.compile()
