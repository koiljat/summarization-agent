
def get_token_count(text: str) -> int:
    """
    Approximate token count for LLM input.
    1 token ≈ 4 characters.
    """
    return len(text) // 4

def count_tokens(state):
    """Count tokens from the parsed_docs"""
    parsed_docs = state.get("parsed_docs", "")
    token_count = len(parsed_docs) // 4  # Rough estimate: 1 token ~ 4 characters
    return {"token_count": token_count}
