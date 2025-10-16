import base64
import io
from PIL import Image
from gradio.themes.builder_app import variable
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from multipart import file_path
from sympy import content
import gradio as gr
from torchgen.gen_functionalization_type import return_from_mutable_noop_redispatch

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

# user_msg = HumanMessage([{'type':'text','text':'你知道机器学习是什么吗，限制字数在30字'}])
config = {"configurable":{"session_id":"str(uuid.uuid4())"}}
#
# resp1 = chain_history.invoke({'message': [user_msg]},config = config)
# print(resp1.content)


def add_message(history, messages):
    """将用户输入的消息添加到聊天记录中"""

    # 处理上传文件
    if messages['files'] is not None:
        for m in messages['files']:
            # print(m)
            history.append({'role':'user','content':{'path':m}})

    # 处理文本消息
    if messages["text"] is not None:
        history.append({
            "role": "user",
            "content": messages["text"]
        })
    # 返回更新后的历史记录 + 重置输入框
    return history, gr.MultimodalTextbox(value='Submit success!', interactive=True)


def get_last_user_after_assistant(history):
    """反向遍历找到最后一个assistant的位置, 并返回后面的所有user消息"""
    if not history:
        return None
    if history[-1]["role"] == "assistant":
        return None

    last_assistant_idx = -1
    for i in range(len(history) - 1, -1, -1):
        if history[i]["role"] == "assistant":
            last_assistant_idx = i
            break

    # 如果没有找到assistant
    if last_assistant_idx == -1:
        return history
    else:
        # 从assistant位置向后查找第一个user
        return history[last_assistant_idx + 1:]

def transcribe_audio(audio_path):
    """使用Base64处理语音转化"""
    """
        注意：目前所有的多模态大模型,如果需要传入多媒体内容。只有两种方式：
        1、传入多媒体文件的网络访问路径，比如：http：//www.baidu.com/log.png
        2、把文媒体文件转化为base64格式的字符串，再传入大模型                    
    """
    try:
        with open(audio_path, 'rb') as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        audio_message = { # 把音频文件封装成一条消息
            "type": "audio_url",
            "audio_url": {
                "url": f"data:audio/wav;base64,{audio_data}",
                "duration": 30  # 单位：秒（帮助模型优化处理）
            }
        }
        return audio_message
    except Exception as e:
        print(e)
        return {}

def transcribe_image(image_path):
    """
        将任意格式的图片转换为 base64 编码的 data URL
        :param image_path: 图片路径
        :return: 包含 base64 编码的字典
    """
    with Image.open(image_path) as img:
        # 获取图片原始格式
        img_format = img.format if img.format else "png"

        buffered =io.BytesIO()

        # 保留原始格式（避免png强制转化导致透明通道丢失）
        img.save(buffered, format=img_format)

        img_data =base64.b64encode(buffered.getvalue()).decode('utf-8')
        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/{img_format.lower()};base64,{img_data}",
                "detail":'low'
            }
        }


def submit_messages(history):
    """提交消息，生成机器人回复"""
    user_messages = get_last_user_after_assistant(history)
    print(user_messages)
    content =[] # HumanMessage的内容
    if user_messages is not None:
        for x in user_messages:
            if isinstance(x['content'],str): # 文字消息
                content.append({'type':'text','text':x['content']})
            elif isinstance(x['content'],tuple): # 多媒体输入消息
                file_path = x['content'][0] # 得到多媒体的文件路径

                if file_path.endswith('.wav') or file_path.endswith('.mp3'): # 输入的是音频文件
                    file_message = transcribe_audio(file_path)
                elif file_path.endswith('.jpg') or file_path.endswith('.png') or file_path.endwith('.jpeg'):  # 输入的是图像文件
                    file_message = transcribe_image(file_path)
                content.append(file_message)
            else:
                pass
    input_message=HumanMessage(content=content)
    resp = chain_history.invoke({'messages':input_message},{'configurable':{"session_id":"str(uuid.uuid4())"}})
    history.append({'role':'assistant','content':resp.content})
    return history

# 开发一个聊天机器人的Web界面
with gr.Blocks(title='多模态聊天机器人', theme="gradio/soft") as block:
    # 聊天历史记录的组件
    chatbot = gr.Chatbot(type = 'messages',height=500,label='聊天机器人',bubble_full_width=False)

    # 创建多模态输入框
    chat_input = gr.MultimodalTextbox(
        interactive=True,# 可交互
        file_types=['.txt','image','.wav','.mp4'],# 允许上传文件格式
        file_count="multiple",# 允许多文件上传
        placeholder="Ask anything u want (^_^)",# 输入框提示文本
        show_label=False,# 不显示标签
        sources=["microphone","upload"],# 支持麦克风和文件上传
    )

    # 提交事件
    chat_input.submit(
        add_message,
        [chatbot, chat_input],
        [chatbot, chat_input]
    ).then(
        submit_messages,
        [chatbot],
        [chatbot]
    )

if __name__ == '__main__':
    block.launch()