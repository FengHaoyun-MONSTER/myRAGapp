import ollama, sys, os, chromadb
from loadText import getconfig

# 向量生成模型与基础大模型
embedmodel = getconfig()["embedmodel"]
llmmodel = getconfig()["mainmodel"]

# 本地向量库
# 向量数据库存储路径处理
script_dir = os.path.dirname(os.path.abspath(__file__)) # 当前脚本所在绝对路径
project_root = os.path.dirname(script_dir) # 上一级目录
chroma_db_path = os.path.join(project_root, 'chroma_db') # 拼接成chroma_db所在的路径，所有的向量与集合会保存到这个路径下


chroma = chromadb.PersistentClient(path=chroma_db_path) # PersistentClient本地持久化客户端，
# chroma.delete_collection(name="ragdb")
collection = chroma.get_or_create_collection(name="ragdb") # get_or_create_collection接口存在就获取，不存在就创建并返回。返回的是collection对象

while True:
    query = input("输入问题： ")
    if not query or query.lower() == 'quit':
        break
    else:
        # 从向量库中查询与问题相似的知识块
        results = collection.query(
            query_embeddings=[ollama.embeddings(model=embedmodel, prompt=query)['embedding']],
            n_results=3,
            include=["documents", "distances", "metadatas"],
        )["documents"][0]

        results = "\n\n".join(results)
        print(results)

        # 生成Prompt
        modelquery = f"""
        你是位学习高手，你要学习以下的上下文，基于上下文回答问题，如果上下文中不存在问题的答案相关信息，请回答'我暂时无法回答这个问题'，不允许自己编造。
        上下文：
        ===
        {results}
        ===
        我的问题是：{query}
        """
        # 传给基础大模型生成
        stream = ollama.generate(model=llmmodel, prompt=modelquery, stream=True)

        # 流式输出生成的结果
        for chunk in stream:
            # chunk 是形如 {"response": "...", "done": bool, ...} 的字典
            if chunk.get("response"):
                print(chunk["response"], end='', flush=True)
        print()  # 每轮回答结束后换行


