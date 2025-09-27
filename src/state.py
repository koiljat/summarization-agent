"""State management for the summarization agent"""

from typing import Union, List, TypedDict, Optional
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage


class AgentState(TypedDict):
    """State schema for the summarization agent"""
    provider: str  # "openai" or "google"
    model: str  # e.g., "gpt-4" or "gemini-2.5-flash"
    temperature: float  # default at 0.0
    max_tokens: int  # default at 4096
    top_p: float  # default at 1.0
    parsed_docs: str
    summary: str
    messages: List[Union[HumanMessage, AIMessage, str]]  # Accepts list of HumanMessage, AIMessage, or str
    summary_type: str  # Few-shot / Map-Reduce / RAG / etc.
    llm: Optional[Union[ChatOpenAI, ChatGoogleGenerativeAI]]  # LLM instance, supports LangChain chat models
    token_count: int  # Token count of the input documents
    summary_plan: str  # Plan for summarization approach
    