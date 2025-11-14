import asyncio
from tkinter.font import names

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from src.llm.claude_4 import llm

# mcp服务端连接配置
python_mcp_server_config={
    # 'url': 'http://localhost:8080/streamable',
    # 'transport': 'streamable_http',
    'url': 'http://localhost:8080/streamable',
    'transport': 'streamable_http',
}

# mcp_client = MultiServerMCPClient(
#     connections={
#         "marvelous_mcp_server": {
#             "transport": "sse",
#             "url": "http://localhost:8080/sse",
#         }
#     }
# )

# mcp客户端
mcp_client = MultiServerMCPClient(
    connections={
        "marvelous_mcp_server": python_mcp_server_config
    }
)

async def mcp_create_agent():
    """必须在异步函数中"""
    mcp_tools = await mcp_client.get_tools()
    print(mcp_tools)

    # p = await mcp_client.get_prompt(
    #     server_name='marvelous_mcp_server',
    #     prompt_name='ask_about_topic',
    #     arguments={
    #         'topic':'AI-Agent开发'
    #     }
    # )
    # print(p)
    #
    # data = await mcp_client.get_resources(
    #     server_name='marvelous_mcp_server',
    #     uris='resource://config',
    # )
    # print(data)

    return create_agent(
        model=llm,
        tools=mcp_tools,
        system_prompt="你是一个智能助手，尽可能的调用工具回答用户的问题",
    )

agent = asyncio.run(mcp_create_agent())
