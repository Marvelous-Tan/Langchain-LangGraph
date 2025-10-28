from langchain.agents import create_agent
from src.agent.tools.tools_4 import calculate4
from src.llm.claude_4 import llm


# def get_weather(city: str) -> str:
#     """Get weather for a given city."""
#     return f"It's always sunny in {city}!"

graph = create_agent(
    model=llm,
    tools=[calculate4],
    system_prompt="You are a helpful assistant"
)