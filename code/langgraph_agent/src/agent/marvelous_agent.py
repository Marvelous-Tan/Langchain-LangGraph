from langchain.agents import create_agent, AgentState
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig

from src.agent.marvelous_state import CustomState
from src.agent.tools.tools_10 import get_user_name, greet_user
from src.agent.tools.tools_4 import calculate4
from src.agent.tools.tools_6 import runnable_tool
from src.agent.tools.tools_7 import claude_search_tool
from src.agent.tools.tools_9 import get_user_info_by_name
from src.llm.claude_4 import llm


# def get_weather(city: str) -> str:
#     """Get weather for a given city."""
#     return f"It's always sunny in {city}!"


# 提示词模版函数：由用户传入内容，组成一个动态的系统提示词
def prompt(state: AgentState,config:RunnableConfig)->list[AnyMessage]:
    user_name = config['configurable'].get('user_name', "Marvelous")
    print(user_name)
    system_message = f'你是一个智能助手,尽可能调用工具回答用户的问题，当前用户的名字是：{user_name}'
    return [{'role':'system','content':system_message}]+state['messages']

# class CustomMiddleware(AgentMiddleware):
#     state_schema = CustomState
#     tools = [tool1, tool2]

graph = create_agent(
    model=llm,
    # tools=[calculate4,runnable_tool,claude_search_tool,get_user_info_by_name],
    tools=[calculate4,runnable_tool,claude_search_tool,get_user_name,greet_user],
    # system_prompt="You are a helpful assistant"
    system_prompt=str(prompt),
    state_schema=CustomState, # 指定自定义状态类
)