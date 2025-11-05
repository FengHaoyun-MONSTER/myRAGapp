# myRAGapp
这是学习RAG应用逻辑的一个简单练习。
<br>虽然现在有LlamaIndex和LangChain框架，只需要几行代码就能实现，但我对其内部逻辑感到好奇。<br>

<br>首先，我在本地部署了向量大模型qwen3-embedding:4b 和基础大语言模型deepseek-r1:7b<br> 
我的电脑配置：
- 💻 设备	联想 Legion Y9000P IAH7H
- ⚙️ CPU	Intel Core i9-12900H（12th Gen）
- 🧠 内存	16 GB DDR5 4800 MHz
- 🎮 GPU	NVIDIA GeForce RTX 3060 Laptop（6 GB 显存）
- 💾 存储	1.38 TB SSD


<br> 其次，这个练习简单的逻辑主要分为：<br>
<br> 加载本地文件 <br>
<br> 简单的分割文件（现实的应用会更好的分割文件）<br>
<br> 把分割好的知识块传给向量模型处理后存入向量数据库 <br>
<br> 问一个问题，先从向量数据库中查出与该问题相关的知识块 <br>
<br> 把知识块放入prompt中，一并发给基础大模型 <br>

