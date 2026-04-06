from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

model = ChatOpenAI(
    base_url="http://192.168.1.2:1234/v1",
    #api_key="lm-studio",  # LMStudio no requiere clave real, pero el campo es obligatorio
    model="qwen/qwen3-4b-thinking-2507",
)

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)


