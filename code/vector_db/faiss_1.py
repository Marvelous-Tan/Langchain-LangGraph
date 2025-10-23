import faiss
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_community.docstore import InMemoryDocstore
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


# 向量数据库不等于关系型数据库
# faiss向量数据库：pip install faiss-cpu / pip install faiss-gpu

# 1、初始化数据库
# 先创建索引的规则
index = faiss.IndexFlatL2(
    len(model.embed_query("hello world")),
)

vector_store = FAISS(
    embedding_function= model,
    index = index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)

# 2、准备数据（Document）

document_1 = Document(
    page_content = "今天早上我喝了一杯美式咖啡，然后去公园散步。",
    metadata={"source": "tweet"},
)

document_2 = Document(
    page_content="明天的天气预报显示可能会下小雨，记得带伞出门。",
    metadata={"source": "news"},
)

document_3 = Document(
    page_content="苹果公司将在下周发布新款MacBook，搭载更强的芯片。",
    metadata={"source": "tech"},
)

document_4 = Document(
    page_content="昨晚我看了一部科幻电影，特效非常震撼。",
    metadata={"source": "blog"},
)

document_5 = Document(
    page_content="今天股市上涨了2%，主要受科技股带动。",
    metadata={"source": "finance"},
)

document_6 = Document(
    page_content="上海外滩夜景依然迷人，游客络绎不绝。",
    metadata={"source": "travel"},
)

document_7 = Document(
    page_content="人工智能正在改变教育行业的教学方式。",
    metadata={"source": "article"},
)

document_8 = Document(
    page_content="午餐我点了一份牛肉拉面和一杯冰绿茶。",
    metadata={"source": "tweet"},
)

document_9 = Document(
    page_content="新冠疫苗的加强针接种工作将在下月启动。",
    metadata={"source": "news"},
)

document_10 = Document(
    page_content="昨晚服务器日志异常，可能是内存泄漏引起的。",
    metadata={"source": "engineering"},
)

document = [document_1, document_2, document_3, document_4, document_5, document_6, document_7, document_8, document_9, document_10, ]
ids = ['id:'+str(i+1) for i in range(len(document))]

vector_store.add_documents(document, ids = ids)

if __name__ == "__main__":
    res=vector_store.similarity_search("天气预报",k=2)
    for resp in res:
        print(type(resp))
        print(f"*{resp.page_content}[{resp.metadata}]")