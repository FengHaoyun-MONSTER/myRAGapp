# 嵌入式的使用方式
# 测试本地chroma是否正常工作
try:
    import chromadb
    print("chroma is installed")
except ImportError:
    print("chroma is not installed")
    exit(1)
client = chromadb.PersistentClient(path=r"E:\myModel\chroma_db")
try:
    client.heartbeat()
    print("client is heartbeat")
except Exception as e:
    print(f"error: {e}")
    exit(1)