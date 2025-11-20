from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="gpt-5-chat",  # Claude 最新模型名
    temperature=0.8,
    api_key="sk-W4xyJa17yfll5gFXNrYDvIaOrcr4dJJyu3GNA2sI1usWgBWK",
    base_url="https://globalai.vip",                 # 你的代理或 Anthropic 官方接口
    extra_headers={
        "anthropic-version": "2023-06-01",  # Anthropic 必需头
    }
)

