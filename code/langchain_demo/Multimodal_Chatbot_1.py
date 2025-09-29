from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from llm.deepseek import llm


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




