from langchain.agents import create_agent, AgentState
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore

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

# class CustomMiddleware(AgentMiddleware):
#     state_schema = CustomState
#     tools_node = [tool1, tool2]

# 初始化数据库
DB_URI = "postgresql://postgres:tlch030206@localhost:5432/marvelous_pgsql?sslmode=disable"
with (
    PostgresSaver.from_conn_string(DB_URI) as checkpointer,
    PostgresStore.from_conn_string(DB_URI) as store,
):
    # checkpointer.setup()
    store.setup()
    agent = create_agent(
        model=llm,
        # tools_node=[calculate4,runnable_tool,claude_search_tool,get_user_info_by_name],
        tools=[runnable_tool,claude_search_tool],
        # system_prompt="You are a helpful assistant"
        system_prompt="你是一个智能助手，尽可能的调用工具回答用户的问题",
        checkpointer=checkpointer, # 短期记忆，保持到内存中，也可以存储在pgsql中
        store=store, # 长期记忆，保存在pgsql中，但是有一个注意点，设置长期记忆的时候必须初始化短期记忆
    )

    config = {"configurable": {"thread_id": "1"}}

    # 从短期存储中返回当前会话上下文
    result1 = list(agent.get_state(config))
    print(result1)

    # 从长期存储中返回历史会话信息
    result2 = list(agent.get_state(config))
    print(result2)

    # resp1=agent.invoke(
    #     input={"messages": [{"role": "user", "content": "北京天气怎么样"}]},
    #     config={"configurable": {"thread_id": "1"}},
    # )
    # print(resp1)
    #
    # resp2=agent.invoke(
    #     input={"messages": [{"role": "user", "content": "那南京呢"}]},
    #     config={"configurable": {"thread_id": "1"}},
    # )
    # print(resp2)