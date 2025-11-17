import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph

from code.langchain_demo.Multimodel_Chatbot_6 import user_input
from src.mcp_server.marvelous_mcp_server_config import python_mcp_12306_server_config
from src.mcp_server.marvelous_mcp_server_config import python_mcp_claude_search_server_config
from src.mcp_server.marvelous_mcp_server_config import python_mcp_table_create_server_config

from src.llm.claude_4 import llm
from src.tools_node.async_tools_node import BasicToolsNode

# mcp客户端
mcp_client = MultiServerMCPClient(
    connections={
        "marvelous_claude_search_mcp_server":python_mcp_claude_search_server_config,
        "marvelous_12306_mcp_server": python_mcp_12306_server_config,
        "marvelous_table_create_mcp_server": python_mcp_table_create_server_config,
    }
)

# 自定义state信息
class State(MessagesState):
    pass

# 定义路由函数
def route_tools_func(state:State):
    """
    动态路由函数，如果从大模型输出后的AIMessage，包含有工具调用的指令，就进入入到工具节点tool_node,否则则结束
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tools_edge: {state}")
    # 如果 ai_message 上存在属性 "tool_calls"
    # 并且这个列表长度 > 0，说明模型在上一轮输出中调用了工具
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"  # 控制流跳转到工具执行节点

    # 如果没有工具要调用，则结束（或走到下一个非工具分支）
    return END

async def create_graph():
    """
    自定义创建工作流
    """
    # 获取mcp服务器中的所有工具
    tools = await mcp_client.get_tools()

    # 创建工作流
    builder= StateGraph(State)

    # 大模型绑定工具,创建大模型决策节点,并添加到工作流中
    llm_with_tools = llm.bind_tools(tools)
    async def chatbot(state: State):
        return {'messages':[await llm_with_tools.ainvoke(state['messages'])]}
    builder.add_node('chatbot', chatbot)

    # 创建工具节点，并添加到工作流中
    tools_node = BasicToolsNode(tools)
    builder.add_node('tools_node', tools_node)

    # 添加条件边，chatbot-->tools_node
    builder.add_conditional_edges(
        source='chatbot',
        path=route_tools_func,
        path_map={'tools': 'tools_node',END:END,}
    )

    builder.add_edge('tools_node', 'chatbot')
    builder.add_edge(START, 'chatbot')

    memory= MemorySaver()
    graph = builder.compile(checkpointer=memory,interrupt_before=['tools_node'])
    return graph

# marvelous_12306search_assistant_workflow= asyncio.run(create_graph())

async def run_graph():
    graph = await create_graph()
    # 配置参数，包含乘客ID和线程ID
    config = {
        "configurable": {
            # 检查点由 session_id 访问（就是会话id）
            "thread_id": "marvelous_tan",
        }
    }

    while True:
        user_input = input('user:')
        resp =await execute_graph(user_input)
        print('AI:',resp)
