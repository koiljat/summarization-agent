
def get_token_count(text: str) -> int:
    """
    Approximate token count for LLM input.
    1 token ≈ 4 characters.
    """
    return len(text) // 4
