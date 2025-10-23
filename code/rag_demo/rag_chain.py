import bs4
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_demo.llm.claude_4 import llm
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_text_splitters import RecursiveCharacterTextSplitter


model_name = "Qwen/Qwen3-Embedding-0.6B"
embedding_model = HuggingFaceEmbeddings(model_name=model_name)

# 构建向量数据库
vector_store =Chroma(
    collection_name='t_agent_blog',
    embedding_function=embedding_model,
    persist_directory='chroma_db/'
)

def create_dense_db():
    """把网络关于Agent的博客数据写入向量数据库"""
    loader = WebBaseLoader(
        web_path=('https://lilianweng.github.io/posts/2023-06-23-agent/',),
        bs_kwargs=dict(
            # pip install beautifulsoup4
            parse_only = bs4.SoupStrainer(
                class_ = ("post-content", "post-title", "post_header")
            )
        )
    )

    docs_list = loader.load()

    # 切块
    # 初始化文本分割器，设置块大小1000，重叠200
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs_list)

    print(f"splits: {len(splits)}")

    # 把切块后的文档存入向量数据库中
    ids = ['id:' + str(i + 1) for i in range(len(splits))]
    vector_store.add_documents(documents=splits, ids=ids)

# create_dense_db()

# ------------------------------------------------------------------------------------------------
# 问题上下文化
# 系统提示词：用于将带有聊天历史的问题转化为独立问题
contextualize_q_system_prompt = (
    "给定聊天历史和最新的用户问题（可能引用聊天历史中的上下文），"
    "将其重新表述为一个独立的问题（不需要聊天历史也能理解）。"
    "不要回答问题，只需在需要时重新表述问题，否则保持原样。"
)

# 创建提示词模版
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human","{input}")
    ]
)

# 创建一个向量数据库的检索器
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# 创建一个上下文感知的检索器,对向量数据库的检索器添加了包装，不仅可以检索知识库的内容，还可以检索上下文
history_aware_retriever = create_history_aware_retriever(
    llm=llm,
    retriever=retriever,
    prompt=contextualize_q_prompt,
)
# ------------------------------------------------------------------------------------------------
### RAG回答问题 ###
# 系统提示词：定义助手的行为和回答规范
rag_system_prompt = (
    "你是一个问答任务助手。"
    "使用以下检索到的上下文来回答问题。"
    "如果不知道答案，就说你不知道。"
    "回答最多三句话，保持简洁。"
    "\n\n"
    "{context}"   # 上下文占位符
)

# 创建基于rag的提示词模版
rag_qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", rag_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human","{input}")
    ]
)

# 创建文档处理链
question_chain = create_stuff_documents_chain(
    llm=llm,
    prompt=rag_qa_prompt,
)

# 创建完整的rag检索链
rag_chain = create_retrieval_chain(
    history_aware_retriever,
    question_chain,
)
# ------------------------------------------------------------------------------------------------

# 创建内存数据库，保存历史聊天记录
store ={}
def get_session_history(session_id: str):
    """从内存中的历史消息列表中，返回当前会话的所有历史消息"""
    # 如果会话id不存在，则创建一个InMemoryChatMessageHistory对象
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory() # 一个用户的历史聊天记录
    return store[session_id]

# 创建带历史记录功能的处理链（自动存储历史聊天记录）
conversational_rag_chain = RunnableWithMessageHistory(
    runnable=rag_chain,
    get_session_history=get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)
# ------------------------------------------------------------------------------------------------

resp1 = conversational_rag_chain.invoke(
    input={"input":"Hello,my name is MarvelousTan?"}, # 用户输入问题
    config={"configurable":{"session_id":"abc123"}},# 使用会话ID"abc123"，保持会话历史
)
print(resp1['answer'])

resp2 = conversational_rag_chain.invoke(
    input={"input":"Tell me what is my name and what is your name"}, # 用户输入问题
    config={"configurable":{"session_id":"abc123"}},# 使用会话ID"abc123"，保持会话历史
)
print(resp2['answer'])

