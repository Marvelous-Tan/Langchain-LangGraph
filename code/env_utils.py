from dotenv import load_dotenv # 加载环境变量
import os

load_dotenv(override=True) # 如果产生冲突，则覆盖

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")

LOCAL_BASE_URL = os.getenv("LOCAL_BASE_URL")

CLAUDE_API_KEY = os.getenv("CLAUDE_4_API_KEY")
CLAUSE_URL = os.getenv("CLAUDE_4_URL")
