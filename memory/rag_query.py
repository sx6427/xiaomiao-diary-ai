import os
import chromadb
from openai import OpenAI

client = OpenAI(
    base_url="https://api.xiaomimimo.com/v1",
    api_key=os.environ.get("MIMO_API_KEY")
)

# 初始化Chroma客户端（本地存储）
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="baby_memories")

def embed_text(text: str) -> list:
    """使用Mimo Embedding API获取文本向量"""
    resp = client.embeddings.create(
        model="mimo-embedding-v1",
        input=text
    )
    return resp.data[0].embedding

def add_memory(doc_id: str, content: str, metadata: dict = None):
    """将一条成长记忆存入向量库"""
    embedding = embed_text(content)
    collection.add(
        ids=[doc_id],
        embeddings=[embedding],
        documents=[content],
        metadatas=[metadata] if metadata else [{}]
    )

def query_memory(question: str, n_results: int = 3):
    """自然语言查询最相关的记忆"""
    q_embedding = embed_text(question)
    results = collection.query(
        query_embeddings=[q_embedding],
        n_results=n_results
    )
    # 只返回文档内容和距离
    output = []
    for doc, dist in zip(results['documents'][0], results['distances'][0]):
        output.append({"content": doc, "relevance": 1 - dist})
    return output

# 初始化一些示例记忆（首次运行时取消注释）
# if collection.count() == 0:
#     add_memory("1", "1岁2个月，宝宝第一次叫妈妈，当时正在喂饭，声音很清晰。", {"date": "2025-03-15"})
#     add_memory("2", "1岁3个月，扶着沙发走了三步，然后笑着扑进爸爸怀里。", {"date": "2025-04-02"})
