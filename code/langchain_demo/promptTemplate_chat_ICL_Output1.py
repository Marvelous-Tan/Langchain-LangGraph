from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder, FewShotChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm.deepseek import llm

example = [
    {
        "input":"2😭2",
        "output":"4"
    },
    {
        "input":"3😭3", 
        "output":"6"
    }
]

# 模版需要和example的input和output一致
base_template = ChatPromptTemplate.from_messages([
    ("user", "{input}"),
    ("assistant", "{output}")
])

# 使用 FewShotChatMessagePromptTemplate 而不是 FewShotPromptTemplate
fewshot_template = FewShotChatMessagePromptTemplate(
    examples=example,
    example_prompt=base_template,
)

final_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个计算器，请根据用户输入的数学表达式计算结果，😭表示加法运算"),
    fewshot_template,
    MessagesPlaceholder("msgs")
])

# chain = final_prompt | llm

# 加入输出解析器
chain = final_prompt | llm | StrOutputParser() # 将大模型的输出解析为字符串
print(chain.invoke({"msgs":[("user", "5😭7")]}))