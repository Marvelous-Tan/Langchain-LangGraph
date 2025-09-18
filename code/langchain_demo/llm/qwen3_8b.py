import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from env_utils import LOCAL_BASE_URL
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="qwen3-8b",
    temperature=0,
    base_url=LOCAL_BASE_URL,
    extra_body={'chat_template_kwargs':{'enable_thinking':True}}
)