from typing import Annotated

from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.types import Command

from src.agent.marvelous_state import CustomState


# class CalculateArgs(BaseModel):
#     a:float = Field(description="第1个需要输入的数字")
#     b:float = Field(description="第2个需要输入的数字")
#     operation:str = Field(description="运算类型，只能是：add、subtract、multiply和divide中的任意一个")

# @tool(
#     name_or_callable='get_user_name',
# )
# def get_user_name(
#         tool_call_id:Annotated[str,InjectedToolCallId],
#         config: RunnableConfig
#     ) -> Command:
#     """ 获取当前用户的username，以便生成祝福语句 """
#
#     user_name = config['configurable'].get('user_name','Marvelous')
#     print(f"传入参数，传入的用户名是:{user_name}")
#     return Command(update={
#         "user_name":user_name, # 更新状态中的用户名
#
#         # 就算是不专门写message，message一样会返回传递，但是如下定义可以打印关键信息、保持id相同
#         "message":[ # 更新一条工具执行后的消息：ToolMessage类型
#             ToolMessage(
#                 content='成功得到了当前用户的名字',
#                 tool_call_id=tool_call_id,
#             )
#         ]
#     })
#
# @tool(
#     name_or_callable='greet_users',
# )
# def greet_user(
#         state:Annotated[CustomState,InjectedState]
# ):
#     """在获取用户的username，生成祝福语句"""
#     user_name = state["user_name"]
#     return f'祝福你{user_name}'


@tool(
    name_or_callable='get_user_name',
)
def get_user_name(
        # tool_call_id:Annotated[str,InjectedToolCallId],
        config: RunnableConfig
    ) -> str:
    """ 获取当前用户的username，以便生成祝福语句 """

    user_name = config['configurable'].get('user_name','Marvelous')
    print(f"传入参数，传入的用户名是:{user_name}")
    # return Command(update={
    #     "user_name":user_name, # 更新状态中的用户名
    #
    #     # 就算是不专门写message，message一样会返回传递，但是如下定义可以打印关键信息、保持id相同
    #     "message":[ # 更新一条工具执行后的消息：ToolMessage类型
    #         ToolMessage(
    #             content='成功得到了当前用户的名字',
    #             tool_call_id=tool_call_id,
    #         )
    #     ]
    # })
    return user_name

@tool(
    name_or_callable='greet_users',
)
def greet_user(
        # state:Annotated[CustomState,InjectedState]
        user_name: str,
):
    """在获取用户的username，生成祝福语句"""
    # user_name = state["user_name"]
    return f'祝福你{user_name}'

