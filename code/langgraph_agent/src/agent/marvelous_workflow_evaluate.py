
from typing import TypedDict, Literal

from langchain_core.output_parsers import StrOutputParser
from langgraph.constants import START, END
from pydantic import BaseModel,Field

from src.llm.claude_4 import llm
from langgraph.graph import StateGraph

# 工作流状态
class State(TypedDict):
    joke:str # 生成的冷笑话内容
    topic:str # 用户指定的主题
    feedback:str # 改进建议
    funny_or_not:str # 幽默评级

# 定义大模型
claude_llm=llm

# 构建一个工作流
builder = StateGraph(State)

# 定义节点函数
def joke_generate(state: State):
    """由大模型生成一个冷笑话的节点"""
    if state.get("feedback", None):
        prompt = f"根据反馈改进笑话: {state['feedback']}\n主题: {state['topic']}"
    else:
        prompt = f"创作一个关于{state['topic']}的笑话"

    # 第一种
    resp = claude_llm.invoke(input=prompt,)
    return {'joke': resp.content}

    # 第二种
    #chain = llm | StrOutputParser
    #resp = chain.invoke(prompt=prompt)
    #return {'joke': resp.content}

# 定义节点函数
def joke_evaluate(state: State):
    """评估状态中的冷笑话"""

    # 定义结构化输出
    class feedback_output(BaseModel):
        """使用此类来结构化输出"""
        grade: Literal["funny", "not funny"] = Field(description="判断笑话是否幽默", examples=["funny", "not funny"])
        feedback: str = Field(description="若不幽默，提供改进建议", examples=["可以加入双关语或者意外结局"])

    structured_claude_llm=claude_llm.with_structured_output(feedback_output)
    output = structured_claude_llm.invoke(
        f"评估此笑话的幽默程度：\n{state['joke']}\n"
        "注意：幽默应包含意外性或巧妙措辞"
    )

    return {
        'feedback': output.feedback,
        'funny_or_not': output.grade,
    }

# 添加节点
builder.add_node('joke_generate', joke_generate)
builder.add_node('joke_evaluate', joke_evaluate)

# 添加有向边
builder.add_edge(START,'joke_generate')
builder.add_edge('joke_generate','joke_evaluate')

# 定义条件边路由函数
def router_builder(state: State):
    """返回下一个要访问节点的名字"""
    if state.get("funny_or_not")=='funny':
        return END
    else:
        return 'joke_generate'

    # 映射字段
    # return "Accepted" if state.get("funny_or_not", None) == "funny" else "Rejected + Feedback"

# 添加条件边
builder.add_conditional_edges('joke_evaluate', router_builder)

workflow = builder.compile()
