from gradio.themes.builder_app import variable
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from sympy import content

from langchain_demo.Multimodel_Chatbot_6 import user_input
from llm.claude_4 import llm

prompt = ChatPromptTemplate.from_messages(
    [
        ('system',"你是一个多模态AI助手，可以处理文本、音频、和图像输入"),
        MessagesPlaceholder(variable_name="message"),
    ]
)

chain = prompt | llm

def get_session_history(session_id: str):
    """从关系型数据库中的历史消息列表中，返回当前会话的所有历史消息"""
    return SQLChatMessageHistory(
        session_id=session_id,
        connection_string="sqlite:///chat_history.db"
    )

chain_history = RunnableWithMessageHistory(
    chain,
    get_session_history
)

user_msg = HumanMessage([{'type':'text','text':'你知道机器学习是什么吗，限制字数在30字'}])
config = {"configurable":{"session_id":"str(uuid.uuid4())"}}

resp1 = chain_history.invoke({'message': [user_msg]},config = config)
print(resp1.content)