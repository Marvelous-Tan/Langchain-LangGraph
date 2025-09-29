import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import MessagesPlaceholder, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import SimpleJsonOutputParser, StrOutputParser
from langchain_core.runnables import Runnable
from pydantic import BaseModel, Field
from typing import Optional
from llm.deepseek import llm

# 生成一个笑话：三个属性

class Response(BaseModel):
    answer: str = Field(description="对用户问题的回答")
    followup_Q: str = Field(description="用户后续可能提出的问题")

runnable = llm.bind_tools([Response]) # 生成的是一个AIMessage对象，包含json对象
resp = runnable.invoke("如何实现一个斐波那契数列")

resp.pretty_print()
print(resp.tool_calls[-1].args)