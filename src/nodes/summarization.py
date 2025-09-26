# src/nodes/summarization.py
import os
import logging
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI


def summarize_node(state):
    load_dotenv()
    logging.info("Starting summarization node...")

    pdf_text = state.get("pdf_text")
    if not pdf_text:
        logging.warning("No PDF text to summarize.")
        return {"summary": "No text available to summarize."}

    logging.info(
        f"Initializing LLM with provider '{state.get('provider', 'gemini')}'..."
    )

    try:
        if state.get("provider") == "openai":

            llm = ChatOpenAI(
                model=state.get("model", "gpt-4"), temperature=0.5, api_key=os.getenv("OPENAI_API_KEY")
            )
        else:
            llm = ChatGoogleGenerativeAI(
                model=state.get("model", "gemini-2.5-flash"),
                temperature=0.5,
                api_key=os.getenv("GOOGLE_API_KEY"),
            )

        prompt = f"Summarize the following text in simple language:\n\n{pdf_text}"
        logging.info(f"Sending text to LLM (length {len(pdf_text)} characters)...")

        response = llm.invoke([HumanMessage(content=prompt)])
        summary = response.content if response else "No summary returned."

        logging.info(f"Received summary (length {len(summary)} characters)")
        return {"summary": summary}

    except Exception as e:
        logging.error(f"Error during summarization: {e}")
        return {"summary": f"Error during summarization: {e}"}
