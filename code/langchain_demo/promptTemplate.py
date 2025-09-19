from langchain_core.prompts import PromptTemplate
from llm.deepseek import llm

# 使用from_template方法创建提示词模板
prompt = PromptTemplate.from_template("What is the capital of {country}?")

# 使用invoke方法填充提示词模板
# res = prompt.invoke({"country":"France"})
# print(res)

# 使用format方法填充提示词模板
# print(prompt.format(country="France"))

# 使用invoke方法填充提示词模板
# res = prompt.invoke({"country":"France"})

chain = prompt | llm

# 使用invoke方法填充提示词模板
print(chain.invoke({"country":"France"}))