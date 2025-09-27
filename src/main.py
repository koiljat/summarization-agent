# src/main.py
import logging
from graph import build_graph
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    """Run the summarization workflow"""
    agent = build_graph()
    
    # Initialize state with all required fields - simplified for compatibility
    initial_state = {
        "provider": os.getenv("PROVIDER", "google"),  # or "openai"
        "model": os.getenv("MODEL", "gemini-2.5-flash"),  # or "gpt-4"
        "temperature": os.getenv("TEMPERATURE", 0.5),
        "max_tokens": os.getenv("MAX_TOKENS", 4096),
        "top_p": os.getenv("TOP_P", 1.0),
        "parsed_docs": "",
        "summary": "",
        "messages": ["Start workflow"],  # Simplified to strings
        "summary_type": "planner-executor",
        "llm": None,  # Will be initialized by the first node
        "token_count": 0,
        "summary_plan": ""
    }

    print("🤖 Starting Summarization Agent with Planner-Executor Pattern")
    print("=" * 60)
    
    final_state = agent.invoke(initial_state)
    
    print("\n--- Final Results ---")
    print(f"Provider: {final_state.get('provider')}")
    print(f"Model: {final_state.get('model')}")
    print(f"Token Count: {final_state.get('token_count', 0)}")
    
    if final_state.get('summary_plan'):
        print("\n📋 Summary Plan:")
        print("-" * 40)
        plan = final_state['summary_plan']
        print(plan[:500] + "..." if len(plan) > 500 else plan)
    
    if final_state.get('summary'):
        print("\n📄 Final Summary:")
        print("-" * 40)
        summary = final_state['summary']
        print(summary[:1000] + "..." if len(summary) > 1000 else summary)
    
    print(f"\n📊 Processing completed successfully!")

if __name__ == "__main__":
    main()
