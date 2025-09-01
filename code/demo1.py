from openai import OpenAI

client = OpenAI(base_url="http://localhost:6006/v1",api_key="XXXX")

response = client.chat.completions.create(
    model='Qwen3-8B',
    messages=[{'role':'user','content':'请介绍一下什么是深度学习'}],
    temperature=0.8,
    presence_penalty=1.5, # 控制模型在生成文本时避免重复使用某些词汇

    # qwen3-8b 特有的参数
    extra_body={'chat_template_kwargs':{'enable_thinking':True}} # 表示是否启用思考模式，启用后模型会先思考再回答
)

print(response.choices[0].message.content)