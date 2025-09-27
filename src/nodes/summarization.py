import logging
import sys
import os

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prompt_manager import prompt_manager

def plan_summary(state):
    """Planner-Executor: Plan the summarization strategy"""
    logging.info("Starting summary planning...")
    
    parsed_docs = state.get("parsed_docs", "")
    llm = state.get("llm")
    
    if not parsed_docs:
        logging.warning("No parsed docs to plan for.")
        try:
            error_msg = prompt_manager.get_prompt("system", "error_messages", "no_document")
        except (KeyError, ValueError):
            error_msg = "No documents to summarize."
        return {"summary_plan": error_msg}
    
    if not llm:
        logging.error("No LLM instance available.")
        try:
            error_msg = prompt_manager.get_prompt("system", "error_messages", "no_llm")
        except (KeyError, ValueError):
            error_msg = "Error: No LLM available for planning."
        return {"summary_plan": error_msg}
    
    # Get the planner prompt from YAML and format it
    planner_prompt = prompt_manager.get_prompt(
        'summarization', 'planner', 'template',
        parsed_docs=parsed_docs
    )
    
    try:
        response = llm.invoke(planner_prompt)
        response_text = response.content if hasattr(response, 'content') else str(response)
        
        messages = state.get("messages", [])
        messages.append(f"Planner: {response_text}")
        
        logging.info(f"Generated summary plan: {len(response_text)} characters")
        
        return {
            "summary_plan": response_text,
            "messages": messages
        }
    
    except Exception as e:
        logging.error(f"Error during planning: {e}")
        return {"summary_plan": f"Error during planning: {e}"}

def summarize(state):
    """Generate final summary based on the plan"""
    logging.info("Starting summarization...")
    
    llm = state.get("llm")
    parsed_docs = state.get("parsed_docs", "")
    summary_plan = state.get("summary_plan", "")
    
    if not llm:
        logging.error("No LLM instance available.")
        try:
            error_msg = prompt_manager.get_prompt("system", "error_messages", "no_llm")
        except (KeyError, ValueError):
            error_msg = "Error: No LLM available for summarization."
        return {"summary": error_msg}
    
    # Get the summarizer prompt from YAML and format it
    summarizer_prompt = prompt_manager.get_prompt(
        'summarization', 'summarizer', 'template',
        parsed_docs=parsed_docs,
        summary_plan=summary_plan
    )
    
    try:
        response = llm.invoke(summarizer_prompt)
        summary = response.content if hasattr(response, 'content') else str(response)
        
        messages = state.get("messages", [])
        messages.append(f"Summarizer: {summary}")
        
        logging.info(f"Generated final summary: {len(summary)} characters")
        
        return {
            "summary": summary,
            "messages": messages
        }
    
    except Exception as e:
        logging.error(f"Error during summarization: {e}")
        return {"summary": f"Error during summarization: {e}"}
