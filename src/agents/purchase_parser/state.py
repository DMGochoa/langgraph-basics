from typing import TypedDict, Any, Optional


class PurchaseState(TypedDict):
    input_text: str
    currency: str
    parsed_data: dict[str, Any]
    response: dict[str, Any]
    error: Optional[str]
