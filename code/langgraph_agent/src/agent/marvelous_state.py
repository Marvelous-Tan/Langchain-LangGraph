from langchain.agents import create_agent, AgentState


# 自己定义的智能体的状态类
class CustomState(AgentState):
    user_name:str # 用户名