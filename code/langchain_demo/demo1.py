from env_utils import OPENAI_API_KEY, OPENAI_BASE_URL, LOCAL_BASE_URL
from langchain_openai import ChatOpenAI

# OpenAI
llm = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0,
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)

'''
# 本地模型
llm = ChatOpenAI(
    model="qwen3-8b",
    temperature=0,
    base_url=LOCAL_BASE_URL,
    extra_body={'chat_template_kwargs':{'enable_thinking':True}}
)
'''
message = [
    ('system', '你是一个助手，请回答用户的问题'),
    ('user', '请介绍一下什么是深度学习'),
]

response = llm.invoke(message) # 将消息传递给模型
print(response.content) # response包含字段content，content包含模型生成的文本
print(response.reasoning_content) # response包含字段reasoning_content，reasoning_content包含模型思考的过程