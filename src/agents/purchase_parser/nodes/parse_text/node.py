from typing import List
from pydantic import BaseModel
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from .prompt import SYSTEM_PROMPT, HUMAN_PROMPT_TEMPLATE


class Item(BaseModel):
    name: str
    quantity: int
    unit_price: float


class ParsedPurchase(BaseModel):
    intent: str
    items: List[Item]
    discount_percent: float


def parse_text_node(state: dict):
    input_text = state.get("input_text", "")
    currency = state.get("currency", "COP")

    if not input_text:
        return {"error": "no_input_text"}

    llm = init_chat_model(
        model="openai:google/gemma-4-e4b",
        base_url="http://100.105.94.89:1234/v1",
    ).with_structured_output(ParsedPurchase)

    human_msg = HUMAN_PROMPT_TEMPLATE.format(input_text=input_text, currency=currency)

    try:
        result: ParsedPurchase = llm.invoke([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=human_msg),
        ])
        return {"parsed_data": result.model_dump()}
    except Exception as e:
        return {"error": f"parse_failed: {e}"}
