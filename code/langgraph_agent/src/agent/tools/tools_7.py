from typing import Any

import anthropic
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from src.llm.claude_4 import llm

class SearchArgs(BaseModel):
    query: str = Field(description='需要搜索网络搜索的信息')

# 网络搜索的工具
class MySearchTool(BaseTool):
    # 工具名字
    name: str = "search_tool"                       # ✅ 添加类型注解
    description: str = "搜索互联网内容的工具"        # ✅ 添加类型注解
    args_schema: type[BaseModel] = SearchArgs       # ✅ 添加类型注解
    return_direct: bool = False                     # ✅ 添加类型注解
    def _run(self, query) -> str:
        client = anthropic.Anthropic(
            api_key="sk-W4xyJa17yfll5gFXNrYDvIaOrcr4dJJyu3GNA2sI1usWgBWK",
            base_url="https://globalai.vip",
        )

        print("执行我的Python中的工具，输入的参数为：",query)
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=512,
            messages=[{
                    "role": "user",
                    "content": query
                }
            ],
            tools=[
                {
                "type": "web_search_20250305",
                "name": "web_search",
                "max_uses": 5
            }
            ]
        )
        return next((b.text for b in reversed(response.content) if b.type == "text"), "")

# 创建工具
claude_search_tool = MySearchTool()

print(claude_search_tool.name)
print(claude_search_tool.description)
print(claude_search_tool.args_schema.model_json_schema())
print(claude_search_tool.return_direct)