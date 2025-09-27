# src/nodes/pdf_parsing.py
import os
import logging
from PyPDF2 import PdfReader


def parse_pdf(state):
    """Parse PDF and extract text content"""
    logging.info("Starting PDF parsing node...")
    
    # Use fixed path for sample PDF
    sample_pdf_path = "data/sample.pdf"  # Adjust path as needed
    
    if not os.path.exists(sample_pdf_path):
        logging.error(f"Sample PDF not found at {sample_pdf_path}")
        return {
            "parsed_docs": "",
            "messages": state.get("messages", []) + [f"System: Error - PDF not found at {sample_pdf_path}"]
        }
    
    try:
        reader = PdfReader(sample_pdf_path)
        text = ""
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            text += page_text + "\n"
            logging.info(f"Parsed page {i+1} with {len(page_text)} characters")
        
        logging.info(f"Successfully parsed PDF: {len(text)} characters total")
        
        messages = state.get("messages", [])
        messages.append(f"System: {text}")
        
        return {
            "parsed_docs": text,
            "messages": messages
        }
    
    except Exception as e:
        logging.error(f"Error reading PDF: {e}")
        return {
            "parsed_docs": "",
            "messages": state.get("messages", []) + [f"System: Error reading PDF - {e}"]
        }
