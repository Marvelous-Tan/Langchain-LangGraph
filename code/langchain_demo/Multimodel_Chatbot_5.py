from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from sqlalchemy.sql.functions import user
from llm.claude_4 import llm
from langchain_community.chat_message_histories.sql import SQLChatMessageHistory
from langchain_core.runnables import RunnablePassthrough
import gradio as gr

# 1、提示词模版
prompt = ChatPromptTemplate.from_messages([
    ("system", "{system_message}"),
    # MessagesPlaceholder 就是 在提示词（prompt）里留一个“插槽”，这个插槽不是放一段字符串，而是放一整段“聊天记录”或者“模型自己的小笔记”
    MessagesPlaceholder(variable_name="chat_history",optional=True), 
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

# 5、剪辑和摘要上下文、历史记录：保留最近的前两条消息，之前所有的消息形成摘要
def sumarize_message(current_input):
    session_id = current_input['config']['configurable']['session_id']
    if not session_id:
        raise ValueError("session_id not found")

    # 获取当前会话ID的所有历史聊天记录
    chat_history = get_session_history(session_id)

    # 获取messages列表
    stored_messages = chat_history.get_messages()
    if len(stored_messages) <= 2:
        return {"original_message":stored_messages, "summary":None} # 不满足条件时直接返回最近原始消息即可
    
    # 剪辑消息列表
    clipped_messages = stored_messages[-2:]

    # 生成摘要
    summarized_messages = stored_messages[:-2]
    summary_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个摘要助手，请根据以下消息生成摘要。"),
        ("placeholder", "{chat_history}"),
        ("human", "请生成包含上述对话核心内容的摘要，保留重要事实和决策。"),
    ])
    
    summary_chain = summary_prompt | llm
    # AIMessage
    summary_message = summary_chain.invoke({"chat_history": summarized_messages})

    # 重建历史聊天记录：清空、添加摘要、添加最后两条消息
    # 但是这样会有一个问题，这样会导致历史记录中永远只有5条信息，但我们只是对过往历史纪录进行摘要而不是将其完全删除，所以该逻辑有bug不可使用
    # chat_history = chat_history.clear()
    # chat_history.add_message(summary_message)
    # for message in clipped_messages:
    #     chat_history.add_message(message)
    
    # return True

    return{
        "original_message":clipped_messages,
        "summary":summary_message
    }
    
# 6、创建最终的链
# RunnablePassthrough 默认会将输入数据原样传递到下游，而.assign()方法允许在保留原始输入的同时
# 通过键值队被函数赋值（如：messages_sumarized=sumarize_message）向输入字典中添加新字段
# messages_sumarized是一个字典，包含original_message和summary
final_chain = RunnablePassthrough.assign(messages_sumarized=sumarize_message) | RunnablePassthrough.assign(
    input = lambda x: x['input'],
    chat_history = lambda x: x['messages_sumarized']['original_message'],
    system_message = lambda x: f"你是一个乐于助人的助手。尽你所能回答所有问题。摘要：{x['messages_sumarized']['summary'].content}" if x['messages_sumarized'].get('summary') else "无摘要"
)|chain_with_message_history

# result1 = final_chain.invoke({"input":"你好，我是小明，请介绍一下你自己","config":{"configurable": {"session_id": "user_1"}}},config={"configurable": {"session_id": "user_1"}})
# print(result1)

# result2 = final_chain.invoke({"input":"我的名字叫什么","config":{"configurable": {"session_id": "user_1"}}},config={"configurable": {"session_id": "user_1"}})
# print(result2)

# result2 = final_chain.invoke({"input":"历史上和我同名的人有哪些","config":{"configurable": {"session_id": "user_1"}}},config={"configurable": {"session_id": "user_1"}})
# print(result2)



# web界面中的核心函数
def add_message(chat_history,user_message):
    if user_message:
        chat_history.append({'role':'user','content':user_message})
    return chat_history,''

# 调用链，使用大模型
def execute_chain(chat_history):
    input = chat_history[-1]['content']
    result = final_chain.invoke({"input":input,"config":{"configurable": {"session_id": "user_1"}}},config={"configurable": {"session_id": "user_1"}})
    chat_history.append({'role':'assistant','content':result.content})
    return chat_history

# 开发一个聊天机器人的Web界面
with gr.Blocks(title='多模态聊天机器人', theme="gradio/soft") as block:
    # 聊天历史记录的组件
    chatbot = gr.Chatbot(type = 'messages',height=500,label='聊天机器人')

    with gr.Row():
        # 文字输入区域
        with gr.Column(scale=4):

            # 文本输入框
            user_input = gr.Textbox(label='文字输入',placeholder='请输入你的问题',max_lines=10)

            # 提交按钮
            submit_button = gr.Button(value = '提交',variant='primary')

        with gr.Column(scale=1):

            # 录制音频
            audio_input = gr.Audio(sources=['microphone'],label='语音输入',type='filepath',format='mp3')
            submit_button = gr.Button(value = '提交',variant='primary')

    chat_msg = user_input.submit(add_message,inputs=[chatbot,user_input],outputs=[chatbot,user_input])
    
    # .then()表示执行完submit之后，再执行下一个函数
    chat_msg.then(execute_chain,inputs=[chatbot],outputs=[chatbot])

if __name__ == "__main__":
    block.launch()