from langchain.embeddings import HuggingFaceBgeEmbeddings

model_name = "BAAI/bge-large-zh-v1.5" # 模型名字
model_kwargs = {'device': 'cpu'} # 使用cpu进行推理
encode_kwargs = {'normalize_embeddings': True} # 是否对向量进行归一化
model = HuggingFaceBgeEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs,
    query_instruction="为这个句子生成表示以用于检索相关文章：" # query_instruction（模型提示语）会在生成 embedding 时，与用户的 query 文本拼接成一个完整输入，送入模型进行编码
)

# 3. 要向量化的文本
text = "你好，世界！"

# 4. 执行向量化
vector = model.embed_query(text)

# 5. 输出结果与维度
print(vector)
print("向量维度：", len(vector))