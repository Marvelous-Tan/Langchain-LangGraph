from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="deepseek-r1",
    temperature=0.8,
    api_key="sk-W4xyJa17yfll5gFXNrYDvIaOrcr4dJJyu3GNA2sI1usWgBWK",
    base_url="https://globalai.vip",
    extra_body={'chat_template_kwargs':{'enable_thinking':True}}
)