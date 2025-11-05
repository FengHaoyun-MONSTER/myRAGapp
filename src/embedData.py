# 把分割很好的句子块传给文本向量大模型生成向量数据，存入向量数据库
import ollama, chromadb
import os

# 引入已经写好的模块
from loadText import loadtext, getconfig
from splitText import split_text_by_sentences

# 向量模型
embedmodel = getconfig()["embedmodel"]


# 向量库
# CS模式
# chroma = chromadb.HttpClient(host="localhost", port=8000) 
# 向量库 - 使用本地持久化存储（嵌入式数据库）

# 向量数据库存储路径处理
script_dir = os.path.dirname(os.path.abspath(__file__)) # 当前脚本所在绝对路径
project_root = os.path.dirname(script_dir) # 上一级目录
chroma_db_path = os.path.join(project_root, 'chroma_db') # 拼接成chroma_db所在的路径，所有的向量与集合会保存到这个路径下


chroma = chromadb.PersistentClient(path=chroma_db_path) # PersistentClient本地持久化客户端，
# chroma.delete_collection(name="ragdb")
collection = chroma.get_or_create_collection(name="ragdb") # get_or_create_collection接口存在就获取，不存在就创建并返回。返回的是collection对象

# 读取文档名列表， 依次处理
# with open('docs.txt','rb') as f:
#     lines = f.readlines()
#     for filename in lines:
        # 加载文档内容

text = loadtext('黄帝内经古文原文白话文译文.txt')

# 把文档分割成知识块
chunks = split_text_by_sentences(source_text=text, sentences_per_chunk=8, overlap=0)

# collection对象add方法需要的参数
ids, embeds, docs, metas = [], [], [], []
for index, chunk in enumerate(chunks):
    embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
    ids.append(f"黄帝内经古文原文白话文译文.txt-{index}")
    embeds.append(embed)
    docs.append(chunk)
    metas.append({"source": "黄帝内经古文原文白话文译文.txt"})
collection.add(ids=ids, embeddings=embeds, documents=docs, metadatas=metas)

    

if  __name__ == "__main__":
    while True:
        query = input("输入问题： ")
        if not query or query.lower() == 'quit':
            break
        else:
            # 从向量库中查询与向量相似的知识块
            results = collection.query(
                query_embeddings=[ollama.embeddings(model=embedmodel, prompt=query)['embedding']],
                n_results=3,
                include=["documents", "distances", "metadatas"],
            )
            # 打印检索到的相关内容（chunk）
            for idx, doc in enumerate(results.get("documents", [[]])[0]):
                print("-------------------")
                print(f"id: {results['ids'][0][idx]}")
                print(f"distance: {results['distances'][0][idx]:.4f}")
                print(f"source: {results['metadatas'][0][idx].get('source', '')}")
                print(doc)
