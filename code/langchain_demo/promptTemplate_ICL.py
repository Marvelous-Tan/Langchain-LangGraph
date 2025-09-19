from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from llm.deepseek import llm



# ICL：要先提供示例，然后让模型根据示例回答问题

# 问题：巴伦·特朗普的父亲是谁
example = [
    {
        'question': '巴伦·特朗普的父亲是谁',
        'answer': '唐纳德·特朗普'
    },
    
    {
        'question': '巴伦·特朗普的母亲是谁',
        'answer': '梅拉尼娅·特朗普'
    }
]


# 步骤一：创建基础模板
base_template = PromptTemplate.from_template(f"问题：{{question}}\n回答：{{answer}}")  
# pyright: ignore[reportUndefinedVariable] 这里是question和answer的变量，由大模型填充

# 步骤二：创建Few-shot示例
final_template = FewShotPromptTemplate(
    examples=example, # 传入示例
    example_prompt=base_template, # 传入基础模板
    suffix=f"问题：{{question}}\n回答：", # 添加前缀，用来填充示例中的question
    input_variables=["question"]  # 这里是用户输入的变量
)

chain = final_template | llm # 将final_template和llm组合成一个chain
print(chain.invoke({"question":"唐朝的前一个朝代是什么"}))