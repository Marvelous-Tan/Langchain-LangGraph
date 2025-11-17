from langchain_anthropic import ChatAnthropic
from env_utils import CLAUDE_API_KEY, CLAUSE_URL  # 注意拼写保持一致

llm = ChatAnthropic(
    model="claude-sonnet-4-5",  # Claude 最新模型名
    temperature=0.8,
    api_key=CLAUDE_API_KEY,
    base_url=CLAUSE_URL,                 # 你的代理或 Anthropic 官方接口
    extra_headers={
        "anthropic-version": "2023-06-01",  # Anthropic 必需头
    }
)