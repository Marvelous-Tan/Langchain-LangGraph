import asyncio
import json
from typing import Dict, Any, List

from langchain_core.messages import ToolMessage, AIMessage
from langgraph.types import interrupt


class BasicToolsNode:
    """
    💡 异步工具节点，用于并发执行 AIMessage 中请求的工具调用

        功能：
            1. 接收工具列表并建立名称索引
            2. 并发执行消息中的工具调用请求
            3. 自动处理同步 / 异步工具适配
    """
    def __init__(self, tools:list):
        """
        初始化工具节点

        Args:
            tools:工具列表，每个工具需包含name属性
        """

        # 所有工具名字的集合，工具名字不重复
        self.tools_by_name={tool.name: tool for tool in tools}

    async def __call__(self, state:Dict[str,Any])->Dict[str,list[ToolMessage]]:
        """
        异步调用入口

        Args:
            state: 输入字典，需包含 "messages" 字段
        Returns:
            包含 ToolMessage 列表的字典
        Raises:
            ValueError: 当输入无效时抛出
        """

        # 1、输入验证
        if not(messages:= state.get('messages')):
            raise ValueError("未能成功获取到Message")
        message:AIMessage = messages[-1] # 获取最新消息：AIMessage

        tool_name = message.tool_calls[0]['name'] if message.tool_calls else None
        if tool_name == "get-tickets":
            resp = interrupt(  # resp(可以是字典)：批准y、或由人工输入的工具执行的大难或者拒绝执行的理由
                f"AI大模型尝试调用工具{tool_name}\n"
                "请审核并选择：批准（y）或者直接给我工具执行的答案"
            )
            if resp["answer"] == "y":
                pass  # 直接使用原参数继续执行
            else:
                return {
                    "messages": [
                        ToolMessage(
                            content=(
                                f"人工终止了该工具的调用，给出的理由或者答案是：{resp['answer']}"
                            ),
                            name=tool_name,
                            tool_call_id=message.tool_calls[0]["id"],
                        )
                    ]
                }

        # 2、并发执行工具调用
        # self调用工具为私有函数
        outputs = await self._execute_tool_calls(message.tool_calls) # tool_calls中可能包含>=1个工具调用
        return {'messages':outputs}

    async def _execute_tool_calls(self, tool_calls: list) -> List[ToolMessage]:
        """执行实际工具调用
        Args:
            tool_calls: 工具调用请求列表

        Returns:
            ToolMessage 结果列表
        """

        async def _invoke_tool(tool_call: Dict) -> ToolMessage:
            """执行单个工具调用
            Args:
                tool_call: 工具调用请求字典，需包含 name/args/id 字段

            Returns:
                封装的 ToolMessage

            Raises:
                KeyError: 工具未注册时抛出
                RuntimeError: 工具调用失败时抛出
            """

            try:
                # 3. 异步调用工具
                tool = self.tools_by_name.get(tool_call["name"]) # 验证工具是否在工具集合中
                if not tool:
                    raise KeyError(f"未注册的工具: {tool_call['name']}")

                # 判断工具是否支持异步调用
                if hasattr(tool, 'ainvoke'):  # 优先使用异步方法
                    tool_result = await tool.ainvoke(tool_call["args"])
                else:  # 同步工具通过线程池转异步
                    loop = asyncio.get_running_loop()
                    tool_result = await loop.run_in_executor(
                        None,  # 使用默认线程池
                        tool.invoke,  # 同步调用方法
                        tool_call["args"]
                    )
                # 4. 构造 ToolMessage
                return ToolMessage(
                    content=json.dumps(tool_result, ensure_ascii=False),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            except Exception as e:
                raise RuntimeError(f"工具调用失败: {tool_call['name']}") from e

        try:
            # 5、并发执行所有工具
            # """
            # asyncio.gather()是python异步编程中用于并发调度多个协程的核心函数
            # 并发执行：所有传入的协程会被同时调度到事件循环中，通过非阻塞 I/O 实现并行处理
            # 结果收集：按输入顺序返回所有协程的结果（或异常），与任务完成顺序无关
            # 异常处理：默认情况下，任一任务失败会立即取消其他任务并抛出异常；若设置 return_exceptions=True，则异常会作为结果返回。
            # """
            return await asyncio.gather(*[_invoke_tool(tool_call)for tool_call in tool_calls])
        except Exception as e:
            raise RuntimeError("并发执行工具时发生错误")from e
