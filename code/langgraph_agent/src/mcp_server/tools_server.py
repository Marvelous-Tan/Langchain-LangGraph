from fastmcp import FastMCP
import anthropic
from langchain_core.tools import BaseTool
from fastmcp.prompts.prompt import TextContent,PromptMessage
from pydantic import BaseModel, Field

mcp_server = FastMCP(
    name="marvelous_mcp_server",
    instructions="mcp_server made of python"
)

@mcp_server.tool(
    name="say_hello"
)
def say_hello(username: str) -> str:
    """给指定的用户打个招呼"""
    return f"Hello, {username}!"


# 变量占位符提示词模版
@mcp_server.prompt()
def ask_about_topic(topic: str) -> str:
    """生成请求解释特定主题的用户消息模板"""
    return f"能否请您解释一下‘{topic}’，这个概念？"


# 高级提示模板：返回结构化消息对象
@mcp_server.prompt()
def generate_code_request(language: str, task_description: str) -> PromptMessage:
    """生成代码编写请求的用户消息模板"""
    content = f"请用{language}编写一个实现以下功能的函数：{task_description}"
    return PromptMessage(
        role="user",
        content=TextContent(type="text", text=content)
    )


# 结构化资源：自动序列化字典为json
@mcp_server.resource(
    uri="resource://config"
)
def get_config()->dict:
    """以json格式返回应用配置"""
    return{
        "theme":"dark",         # 界面主题配置
        "version":"1.2.0",          # 当前版本号
        "features":["tools_node","resources"],   # 已启用的功能模块
    }