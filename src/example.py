#!/usr/bin/env python3
"""
Simple example showing how to use the summarization agent with different configurations
"""

import logging
from graph import build_graph
from state import AgentState

def summarize_with_config(pdf_dir: str = "data", model: str = "gemini-2.5-flash"):
    """
    Run summarization with custom configuration
    
    Args:
        pdf_dir: Directory containing PDF files
        model: Model to use for summarization
        
    Returns:
        Final state with summary
    """
    logging.info(f"Starting summarization with model: {model}")
    
    # Build the agent graph
    agent = build_graph()
    
    # Create initial state
    initial_state: AgentState = {
        "pdf_dir": pdf_dir,
        "model": model,
        "provider": None,
        "pdf_text": None,
        "token_count": None,
        "summary": None,
        "messages": []
    }
    
    # Run the agent
    final_state = agent.invoke(initial_state)
    return final_state

def main():
    """Run example summarizations"""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    
    print("🤖 PDF Summarization Agent - Simple Example")
    print("=" * 50)
    
    # Example 1: Default configuration
    print("\n📄 Example 1: Default summarization")
    result = summarize_with_config()
    
    if result.get("summary"):
        print("\n✅ Summary generated successfully!")
        print(f"📊 Stats: {result.get('token_count', 0)} tokens processed")
        print(f"📝 Summary length: {len(result['summary'])} characters")
        print("\n📋 Summary:")
        print("-" * 40)
        print(result["summary"])
        print("-" * 40)
    else:
        print("❌ No summary generated")
        if result.get("messages"):
            print("Messages:", result["messages"])
    
    # Example 2: Show state information
    print(f"\n🔍 Processing Details:")
    print(f"   PDF Directory: {result.get('pdf_dir')}")
    print(f"   Model Used: {result.get('model')}")
    print(f"   Provider: {result.get('provider')}")
    print(f"   Token Count: {result.get('token_count')}")
    print(f"   Text Length: {len(result.get('pdf_text', '')) if result.get('pdf_text') else 0} chars")
    
    if result.get("messages"):
        print(f"   Messages: {result['messages']}")

if __name__ == "__main__":
    main()