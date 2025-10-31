from typing import Annotated

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool



# class CalculateArgs(BaseModel):
#     a:float = Field(description="第1个需要输入的数字")
#     b:float = Field(description="第2个需要输入的数字")
#     operation:str = Field(description="运算类型，只能是：add、subtract、multiply和divide中的任意一个")

@tool(
    name_or_callable='get_user_info_by_name',
)
def get_user_info_by_name(config: RunnableConfig) -> dict:
    """ 获取用户的所有信息，包括性别，年龄等 """

    user_name = config['configurable'].get('user_name','Marvelous')
    print(f"传入参数，传入的用户名是:{user_name}")
    return {'user_name':user_name,'sex':'男','age':18}


