from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import AIMessage
from typing import TypedDict

class State(TypedDict):
    customer_name: str
    my_age: int
    messages: list[MessagesState]

def node_1(state: State) -> State:
    history = state.get("messages", [])
    if state.get("customer_name") is None:
        return {"customer_name": "Alice"}
    else:
        ai_message = AIMessage(content="Hello, what can I do for you?")
        return {
            "messages": history + [ai_message]
        }

builder = StateGraph(State)
builder.add_node("node_1", node_1)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

agent = builder.compile()