from langchain_core.prompts import PromptTemplate
from src.llm.deepseek import llm

resp = llm.invoke("hello")
print(resp.content)