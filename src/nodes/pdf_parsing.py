# src/nodes/pdf_parsing.py
import os
import logging
from PyPDF2 import PdfReader
from utils import get_token_count


def parse_pdf_node(state):
    logging.info("Starting PDF parsing node...")

    pdf_dir = state.get("pdf_dir", "data")

    if not os.path.exists(pdf_dir):
        logging.warning(f"PDF directory '{pdf_dir}' does not exist.")
        return {
            "messages": state.get("messages", []) + ["PDF directory does not exist."],
            "pdf_text": "",
            "token_count": 0,
        }

    files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]

    if not files:
        logging.warning("No PDF found in directory.")
        return {
            "messages": state.get("messages", []) + ["No PDF found in directory."],
            "pdf_text": "",
            "token_count": 0,
        }

    pdf_path = os.path.join(pdf_dir, files[0])
    logging.info(f"Reading PDF file: {pdf_path}")

    try:
        reader = PdfReader(pdf_path)
        text = ""
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            text += page_text
            logging.info(f"Parsed page {i+1} with {len(page_text)} characters")

        token_count = get_token_count(text)
        logging.info(
            f"Finished parsing PDF: {files[0]} ({len(text)} chars, ~{token_count} tokens)"
        )

        return {"pdf_text": text, "token_count": token_count}

    except Exception as e:
        logging.error(f"Error reading PDF: {e}")
        return {
            "messages": state.get("messages", []) + [f"Error reading PDF: {e}"],
            "pdf_text": "",
            "token_count": 0,
        }
