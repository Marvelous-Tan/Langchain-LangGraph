import asyncio

from langchain_core.messages import ToolMessage, AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph
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

    def print_message(event, result):
        """格式化输出消息"""

        messages = event.get('messages')
        if messages:
            if isinstance(messages, list):
                message = messages[-1]  # 如果消息是列表，则取最后一个

            if message.__class__.__name__ == 'AIMessage':
                if message.content:
                    # print(result)
                    result = message.content  # 需要展示的消息

                msg_repr = message.pretty_repr(html=True) # 转成一个“格式化后的可阅读字符串”

                if len(msg_repr) > 1500:
                    msg_repr = msg_repr[:1500] + " ...（已截断）"  # 超过最大长度则截断

                print(msg_repr)  # 输出消息的表示形式

        return result

    def get_answer(tool_message, user_answer):
        """让人工介入，并且给一个问题的答案"""

        tool_name = tool_message.tool_calls[0]['name']
        answer = (
            f"人工强制终止了工具：{tool_name} 的执行，拒绝的理由是：{user_answer}"
        )

        # 创建一个消息
        new_message = [
            ToolMessage(
                content=answer,
                tool_call_id=tool_message.tool_calls[0]['id']
            ),
            AIMessage(content=answer)
        ]
        # 把新人为造的消息，添加到工作流的 state 中
        graph.update_state(  # 手动修改 state
            config=config,
            values={"messages": new_message}
        )

    async def execute_graph(user_input:str)->str:
        """
        执行工作流的函数

        执行流程：
            如果用户回复不为'y'的话，考虑是否还有下一步工具调用流程：
                如果有，则说明正处在，中断状态下：
                    则输出消息：人工强制终止了工具......
                如果没有，说明不处在，中断状态下：
                    则将用户的恢复作为最新的提示词进行下一轮会话

            如果用户的回复为'y'的话，则中断结束，开始调用工具
        """

        result = ""  # AI助手的最后一条消息
        if user_input.strip().lower() !='y': # 将用户输入的字符串前后空格、换行等字符串删去，然后将字符串小写化
            current_state= graph.get_state(config)
            if current_state.next: # 如果有下一步，说明当前正处在中断状态中
                tools_script_message = current_state.values['messages'][-1] # state中存储的最后一条AIMessage
                # 通过提供关于请求的更改/改变主意的指示来满足工具调用
                get_answer(tools_script_message, user_input)
                message= graph.get_state(config).values['messages'][-1]
                result = message.content
                return result
            else:
                async for chunk in graph.astream({'messages':('user',user_input)},config,stream_mode='values'):
                    result = print_message(chunk, result)
        else: # 用户输入了'y',想继续工具的调用
            async for chunk in graph.astream(None,config,stream_mode='values'):
                result = print_message(chunk,result)

        current_state= graph.get_state(config)
        if current_state.next: # 出现了工作流的中断
            ai_message = current_state.values['messages'][-1]
            tool_name =ai_message.tool_calls[0]['name']
            # ai_message.tool_calls[0]['args']
            result = f"AI助手马上根据你的要求，执行{tool_name}工具。你是否批准继续执行？输入'y'继续，否则请说明您额外的需求。\n"

        return result


    while True:
        user_input = input('user:')
        resp =await execute_graph(user_input)
        print('AI:',resp)

if __name__ == '__main__':
    asyncio.run(run_graph())

