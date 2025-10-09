from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from llm.qwen3_8b import llm
from langchain_community.chat_message_histories.sql import SQLChatMessageHistory


# 1、提示词模版
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个智能助手，尽可能的调用工具回答用户的问题"),
    MessagesPlaceholder(variable_name="chat_history",optional=True), 
    # MessagesPlaceholder 就是 在提示词（prompt）里留一个“插槽”，这个插槽不是放一段字符串，而是放一整段“聊天记录”或者“模型自己的小笔记”
    ("human", "{input}"),
    #MessagesPlaceholder(variable_name="agent_scratchpad",optional=True), # 一般agent开发才会使用到
])

# 2、创建chain
chain = prompt | llm

# 3、存储聊天记录：内存、关系型数据库或者redis数据库
 
# 3.1 存储在内存中
# 用字典来存储聊天记录，key是会话id（session_id）
# 存储的是所有用户的所有历史聊天记录
# store ={}


def get_session_history(session_id: str):
    """从关系型数据库中的历史消息列表中，返回当前会话的所有历史消息"""
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string="sqlite:///chat_history.db"

    )

# SystemMessage,HumanMessage,AIMessage,ToolMessage
# 系统提示词、用户每次输入消息提供提示词、大模型响应返回消息、工具调用返回消息
# 都继承BaseMessage

# 4、创建带历史记录功能的处理链（自动存储历史聊天记录）
chain_with_message_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

result1 = chain_with_message_history.invoke({"input":"你好，我是小明，请介绍一下你自己"},config={"configurable": {"session_id": "user_1"}})
print(result1)

result2 = chain_with_message_history.invoke({"input":"我的名字叫什么"},config={"configurable": {"session_id": "user_1"}})
print(result2)