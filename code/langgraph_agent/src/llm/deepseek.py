from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="DeepSeek-R1-0528-Qwen3-8B",
    temperature=0.8,
    api_key="XXX",
    base_url="http://localhost:6006/v1",
    extra_body={'chat_template_kwargs':{'enable_thinking':True}}
)