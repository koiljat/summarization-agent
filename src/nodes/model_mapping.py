import logging
import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

def initialize_agent_state(state):
    """Initialize the agent state with LLM instance"""
    logging.info("Initializing agent state...")
    
    provider = state.get("provider", "google")
    model = state.get("model", "gemini-2.5-flash")
    temperature = state.get("temperature", 0.5)
    
    logging.info(f"Provider: {provider}, Model: {model}")
    
    if provider == "openai":
        llm = ChatOpenAI(
            model=model,
            temperature=temperature,
        )
    else:
        llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            api_key=os.getenv("GOOGLE_API_KEY"),
        )
    
    return {
        "llm": llm
    }
