from fastmcp import FastMCP
from anthropic import Anthropic

mcp_claude_search_server = FastMCP(
    name="python_mcp_12306_server",
    instructions="mcp_server for web search",
)


@mcp_claude_search_server.tool()
def web_search(query: str) -> str:
    """
    使用 Claude Sonnet 4.5 的 web_search 工具联网搜索。

    输入：query（str）——搜索/提问内容
    输出：Claude 最终给你的纯文本回答（str）
    """
    print("执行我的Python中的工具，输入的参数为:", query)

    # 建议用环境变量管理 key / base_url
    client = Anthropic(
        api_key="sk-W4xyJa17yfll5gFXNrYDvIaOrcr4dJJyu3GNA2sI1usWgBWK",
        base_url="https://globalai.vip",
    )

    response = client.messages.create(
        model="claude-sonnet-4-5",   # 和你截图里的模型一致
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": query,
            }
        ],
        tools=[
            {
                "type": "web_search_20250305",  # 截图里的 type
                "name": "web_search",
                "max_uses": 5,
            }
        ],
    )

    # 提取最后一段 text 类型的内容作为返回值（str）
    for block in reversed(response.content):
        if getattr(block, "type", None) == "text":
            return block.text

    # 如果没有 text，就返回空字符串，保证输出也是 str
    return ""