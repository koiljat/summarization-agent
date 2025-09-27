import logging

def plan_summary(state):
    """Planner-Executor: Plan the summarization strategy"""
    logging.info("Starting summary planning...")
    
    parsed_docs = state.get("parsed_docs", "")
    llm = state.get("llm")
    
    if not parsed_docs:
        logging.warning("No parsed docs to plan for.")
        return {"summary_plan": "No documents to summarize."}
    
    if not llm:
        logging.error("No LLM instance available.")
        return {"summary_plan": "Error: No LLM available for planning."}
    
    planner_prompt = f"""Human:
    You are an award-winning editor specializing in summarizing technical documents for a broad audience. You are given a document enclosed in <document></document>. Your task is to create a strategy for summarizing this document. This strategy will serve as a set of instructions or prompts to guide other editors in producing the final summary.

    Specifically, you should:
    1. Provide a concise overview of the technical document.
    2. Identify sections that may be complex, technical, or challenging for readers.
    3. Suggest strategies or approaches for summarizing these difficult sections effectively.

    <document>{parsed_docs}</document>

    Assistant:"""
    
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
        return {"summary": "Error: No LLM available for summarization."}
    
    summarizer_prompt = f"""Human:
    You are an award-winning editor specializing in summarizing technical documents for a broad audience. You are given a document enclosed in <document></document> and a summarization strategy enclosed in <strategy></strategy>. Your task is to create a summary of the document based on the provided strategy.

    <document>{parsed_docs}</document>
    <strategy>{summary_plan}</strategy>

    Assistant:"""
    
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
