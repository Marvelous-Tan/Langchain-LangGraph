import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import MessagesPlaceholder, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from typing import Optional
from llm.deepseek import llm

# 生成一个笑话：三个属性

# 使用pydantic定义一个类，用于规范输出结构
class joke(BaseModel):
    """笑话结构类"""
    setup: str = Field(description="笑话的设置部分") # 笑话的设置部分
    punchline: str = Field(description="笑话的包袱部分/笑点") # 笑话的包袱部分
    rating: Optional[int] = Field(description="笑话的有趣程度评分，范围是1-10") # 笑话的评分


llmdk = llm.with_structured_output(joke) # 将大模型的输出解析为joke类

prompt = PromptTemplate.from_template("生成一个关于 {president} 的笑话,请将答案控制在100个字符以内")

chain = prompt | llmdk

resp = (chain.invoke({"president":"特朗普"}))
print(resp)

# 将resp转换为json
resp = json.loads(resp)
print(resp)