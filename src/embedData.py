# 把分割很好的句子块传给文本向量大模型生成向量数据，存入向量数据库
import ollama, chromadb
import os

# 引入已经写好的模块
from loadText import loadtext, getconfig
from splitText import split_text_by_sentences

# 向量模型
embedmodel = getconfig()["embedmodel"]

# 向量库 - 使用本地持久化存储（嵌入式数据库）
# 向量库
# chroma = chromadb.HttpClient(host="localhost", port=8000) 
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
chroma_db_path = os.path.join(project_root, 'chroma_db')
chroma = chromadb.PersistentClient(path=chroma_db_path)
# chroma.delete_collection(name="ragdb")
collection = chroma.get_or_create_collection(name="ragdb")

# 读取文档列表， 依次处理
# with open('docs.txt','rb') as f:
#     lines = f.readlines()
#     for filename in lines:
        # 加载文档内容
text = loadtext('黄帝内经古文原文白话文译文.txt')
        # 把文档分割成知识块
chunks = split_text_by_sentences(source_text=text, sentences_per_chunk=8, overlap=0)
        # 用向量大模型对知识块依次处理
for index, chunk in enumerate(chunks):
    embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
# 把处理好的数据存入向量库中
collection.add(['黄帝内经古文原文白话文译文.txt'+str(index)],[embed],documents=[chunk],metadatas={"souorce": '黄帝内经古文原文白话文译文.txt'})

if  __name__ == "__main__":
    while True:
        query = input("输入问题： ")
        if query.lower() == 'quit':
            break
        else:
            # 从向量库中查询与向量相似的知识块
            results = \
collection.query(query_embeddings=[ollama.embeddings(model=embedmodel, prompt=query)['embedding']], n_results=3)
        # 打印文档内容（chunk）
        for result in results["documents"][0]:
            print("-------------------")
            print(result)
