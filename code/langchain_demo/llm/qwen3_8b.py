import sys
import os
from code.env_utils import LOCAL_BASE_URL
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="Qwen3-8B",
    temperature=0,
    base_url=LOCAL_BASE_URL,
    extra_body={'chat_template_kwargs':{'enable_thinking':True}}
)