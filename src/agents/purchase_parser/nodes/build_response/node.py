def build_response_node(state: dict):
    parsed = state.get("parsed_data", {})
    currency = state.get("currency", "COP")

    return {"response": {**parsed, "currency": currency}}
