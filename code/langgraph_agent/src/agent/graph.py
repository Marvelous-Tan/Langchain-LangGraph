from langgraph.prebuilt import create_react_agent

from langchain.agents import create_agent
from src.llm.claude_4 import llm


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

graph = create_agent(
    model=llm,
    tools=[get_weather],
    system_prompt="You are a helpful assistant"
)