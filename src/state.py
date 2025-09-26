"""State management for the summarization agent"""

from typing import Dict, Any, List, Optional, TypedDict


class AgentState(TypedDict):
    """State schema for the summarization agent"""
    # Input configuration
    pdf_dir: str
    model: str
    
    # Processing state
    provider: Optional[str]
    pdf_text: Optional[str]
    token_count: Optional[int]
    summary: Optional[str]
    messages: List[str]
    