import asyncio
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from src.llm.claude_4 import llm

# 获得的token
test_token= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXZfdXNlciIsImlzcyI6Imh0dHBzOi8vd3d3Lm1hcnZlbG91cy5jb20iLCJpYXQiOjE3NjI1MDIxODYsImV4cCI6MTc2MjUwNTc4NiwiYXVkIjoibWFydmVsb3VzX21jcF9zZXJ2ZXIiLCJzY29wZSI6Ik1hcnZlbG91c1RhbiBpbnZva2VfdG9vbHMifQ.tjmSEAYPY9vRtLV5xy9G07_7bDrr71v-liAeGvjJXEJZMwI2KeBcTQ28G70aq7GAmARW-djOFi24UbMKfnYRt20arjqxvEniW1VDG39Ah8QraBG9hkPUqY8dwmwBaKeNwInkyjK-pDjho6KIF5SIaN9cj4eHMLsMJ-AHjmw6UyDxzhVLFu6OqGOk-utu0QEqQZMtGVh_dD5bx4uW2YlMu0oQK2sAymzvvr40CMjFGf1VX7Tr94ndxpIsZfHHRqxL2yz4Gp8nTIM0whpzyKdYXeC-D-0SiRvKnLTBeI_b3sCQju7VshE7Jwy6D9VgBLprAb_ryK01dKDxngm766Dk-Q"

# mcp服务端连接配置
python_mcp_server_config={
    # 'url': 'http://localhost:8080/streamable',
    # 'transport': 'streamable_http',
    'url': 'http://localhost:8080/streamable',
    'transport': 'streamable_http',
    'headers':{
        'Authorization': f'Bearer {test_token}',
    },
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
