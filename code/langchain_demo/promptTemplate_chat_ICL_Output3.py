import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import MessagesPlaceholder, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import SimpleJsonOutputParser, StrOutputParser
from pydantic import BaseModel, Field
from typing import Optional
from llm.deepseek import llm

# 生成一个笑话：三个属性

prompt = ChatPromptTemplate.from_messages([
    "你是一个非常牛逼的代码助手"
    "你必须始终输出一个包含answer和followup_Q两个字段的json对象，其中answer是代码的答案，followup_Q是后续的提问"
    "你不能输出任何其他内容，否则会触发检查"
    "用户输入：{input}"
    "你输出："
])

chain = prompt | llm | SimpleJsonOutputParser()

print(chain.invoke({"input":"如何实现一个斐波那契数列"}))