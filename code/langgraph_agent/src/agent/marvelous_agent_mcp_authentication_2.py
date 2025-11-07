import asyncio

from docutils.nodes import description
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from src.llm.claude_4 import llm

# 获得的token
test_token= "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXZfdXNlciIsImlzcyI6Imh0dHBzOi8vd3d3Lm1hcnZlbG91cy5jb20iLCJpYXQiOjE3NjI1MDQ5NjUsImV4cCI6MTc2MjUwODU2NSwiYXVkIjoibWFydmVsb3VzX21jcF9zZXJ2ZXIiLCJzY29wZSI6Ik1hcnZlbG91c1RhbiBpbnZva2VfdG9vbHMifQ.MAG7sPIBq3xQYNEwI-b5wWQnm3nvSO29oJSTiAKnK56a6p36pphmEO5bd8YY9SwNiZAwsXL0jSoKaqDsM-hWvA5poqOdhgPVsXb0cFShSZJmaGk28uDjNGLcXJb4NgLxKDSzi9XT6ya6RpEFgifnxnrzhhLYyzB6X23d8ro0EublK-PhHsY5YyiUR4ufeRY7vxLA2z6K7BBLTNrzg6PE8nzPp_U_bj7MvFEJhkusegTHT9Z7dIxbLxWcXG0_JPku4VuTLSWRC8tvqb1_nmzt7kyvM3pqFdy-6arsbJXAbEoPTci9oP8zSvDhlwaGp9uLLzan9pQIDkZrhzJvUmXxrQ"
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

    agent =create_agent(
        model=llm,
        tools=mcp_tools,
        system_prompt="你是一个智能助手，尽可能的调用工具回答用户的问题",
    )

    resp = await agent.ainvoke(
        input={
            "messages":[
                {"role":"user","content":"向MarvelousTan问好"}
            ]
        }
    )

    print(resp)
    print(resp['messages'])
    print(resp['messages'][-1].content)

if __name__ == '__main__':
    asyncio.run(mcp_create_agent())