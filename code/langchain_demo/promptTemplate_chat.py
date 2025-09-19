from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.chat import MessagesPlaceholder
from llm.deepseek import llm


# 使用chat模板
# 变量占位符
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个幽默的电台主持人"),
    ("user", "请幽默的介绍一下{input}"),
])

# 消息占位符
prompt1 = ChatPromptTemplate.from_messages([
    ("system", "你是一个幽默的电台主持人"),
    MessagesPlaceholder("msgs")
])

# prompt1.invoke({"msgs":[("user", "请幽默的介绍一下深度学习")]})

# print(prompt.invoke({"input":"深度学习"}))

# print(prompt.format_messages({"input":"深度学习"}))

chain = prompt1 | llm
print(chain.invoke({"msgs":[("user", "请幽默的介绍一下深度学习")]}))