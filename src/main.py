# src/main.py
import logging
from graph import build_graph
from state import AgentState

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    agent = build_graph()
    initial_state: AgentState = {
        "pdf_dir": "data",
        "model": "gemini-2.5-flash",
        "provider": None,
        "pdf_text": None,
        "token_count": None,
        "summary": None,
        "messages": []
    }

    final_state = agent.invoke(initial_state)
    print("\n--- Final State ---")
    for k, v in final_state.items():
        if k != "pdf_text":  # Skip printing full PDF text
            print(f"{k}: {v}")
        else:
            print(f"{k}: [Text length: {len(v) if v else 0} characters]")

if __name__ == "__main__":
    main()
