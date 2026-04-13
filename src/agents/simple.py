from langgraph.graph import StateGraph, START, END, MessagesState
from langchain.chat_models import init_chat_model
import random
from langchain_core.messages import AIMessage
from typing import TypedDict

llm = init_chat_model(
    model="openai:qwen/qwen3-4b-thinking-2507",
    base_url="http://192.168.1.2:1234/v1",
    temperature=0.7,
)

class State(TypedDict):
    customer_name: str
    my_age: int
    messages: list[MessagesState]

def node_1(state: State) -> State:
    history = state.get("messages", [])
    new_state: State = {}
    if state.get("customer_name") is None:
        new_state["customer_name"] = "Alice"
    else:
        new_state["my_age"] = random.randint(20, 50)
    print(new_state)
    print(history)
    ai_message = llm.invoke(history)
    new_state["messages"] = [ai_message]
    
    return new_state

builder = StateGraph(State)
builder.add_node("node_1", node_1)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

agent = builder.compile()