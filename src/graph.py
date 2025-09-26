from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import get_model_provider, parse_pdf_node, summarize_node, finish_node

def should_summarize(state):
    """Conditional routing function"""
    token_count = state.get("token_count", 0)
    if token_count > 1000:
        return "summarize"
    else:
        return "finish"

def build_graph():
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("map_model", get_model_provider)
    graph.add_node("parse_pdf", parse_pdf_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("finish", finish_node)

    # Entry point
    graph.set_entry_point("map_model")

    # Define edges
    graph.add_edge("map_model", "parse_pdf")
    
    # Conditional edge from parse_pdf
    graph.add_conditional_edges(
        "parse_pdf",
        should_summarize,
        {
            "summarize": "summarize",
            "finish": "finish"
        }
    )
    
    graph.add_edge("summarize", "finish")
    graph.add_edge("finish", END)

    return graph.compile()
