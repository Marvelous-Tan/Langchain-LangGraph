from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from pydantic import Field, BaseModel


from src.llm.claude_4 import llm

prompt = (  # 外层的模板
    PromptTemplate.from_template(
        "帮我生成一个简短的，关于{topic}的报幕词。"
        + ", 要求： 1、内容搞笑一点； "
        + "2、输出的内容采用{language}。"
    )
)

chain = prompt | llm | StrOutputParser()

class ToolArgs(BaseModel):
    topic:str = Field(description="报幕词的topic")
    language:float = Field(description="报幕词采用的language")

runnable_tool = chain.as_tool(
    name='chain_tool',
    description='这是一个专门生成报幕词的工具',
    args_schema=ToolArgs
)

