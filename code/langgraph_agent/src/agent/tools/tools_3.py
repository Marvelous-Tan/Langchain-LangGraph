from typing import Annotated

from langchain_core.tools import tool
from pydantic import BaseModel, Field


# class CalculateArgs(BaseModel):
#     a:float = Field(description="第1个需要输入的数字")
#     b:float = Field(description="第2个需要输入的数字")
#     operation:str = Field(description="运算类型，只能是：add、subtract、multiply和divide中的任意一个")

@tool(
    name_or_callable='calculate',
)
def calculate3(
        a:Annotated[float,"第1个需要输入的数字"],
        b:Annotated[float,"第2个需要输入的数字"],
        operation:Annotated[str,"运算类型，只能是：add、subtract、multiply和divide中的任意一个"]

) -> float:

    """工具函数：计算两个数字的运算结果"""

    print(f"调用 calculate 工具，第一个数字: {a}, 第二个数字: {b}, 运算类型: {operation}")

    result = 0.0
    match operation:
        case "add":
            result = a + b
        case "subtract":
            result = a - b
        case "multiply":
            result = a * b
        case "divide":
            if b != 0:
                result = a / b
            else:
                raise ValueError("除数不能为零")
        case _:
            raise ValueError("不支持的运算类型")

    return result

# print(calculate2.name)
# print(calculate2.description)
# print(calculate2.args)
# print(calculate2.args_schema)
# print(calculate2.args_schema.model_json_schema())
# print(calculate2.return_direct)
# print(calculate2.invoke({'a':1, 'b':2, 'operation':'add'}))
