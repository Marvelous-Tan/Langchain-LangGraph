from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. 选择模型（BGE 中文大模型）
model_name = "Qwen/Qwen3-Embedding-0.6B"

# 2. 初始化 LangChain 的嵌入模型
embedding = HuggingFaceEmbeddings(model_name=model_name)

# 3. 要向量化的文本
text = "你好，世界！"

# 4. 执行向量化
vector = embedding.embed_query(text)

# 5. 输出结果与维度
print(vector)
print("向量维度：", len(vector))