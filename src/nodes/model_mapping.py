import logging

def get_model_provider(state):
    logging.info("Starting model mapping node...")

    model = state.get("model", "gemini-2.5-flash")
    logging.info(f"Model selected: {model}")

    mapping = {
        "gemini-2.5-flash": "gemini",
        "gpt-4": "openai",
    }

    provider = mapping.get(model, "gemini")
    if model not in mapping:
        logging.warning(f"Unknown model '{model}', defaulting to 'gemini'")

    logging.info(f"Provider set to: {provider}")

    return {"provider": provider}
