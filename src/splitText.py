import jieba # jieba模块用来分词
import re
# 参数说明：source_text: 源文本, sentences_per_chunk: 允许每个知识块中的句子数, overlap: 两个知识块的允许重叠的句子数
def split_text_by_sentences(source_text: str, sentences_per_chunk: int, overlap: int) -> list[str]:
    """先简单的把文档分割成多个知识块"""
    if source_text is None:
        raise ValueError("source_text 不能为 None")
    if sentences_per_chunk < 2:
        raise ValueError("一个句子至少要有两个chunk")
    if overlap < 0 or overlap >= sentences_per_chunk -1:
        raise ValueError("overlap参数必须大于等于0,且小于sentences_per_chunk -1") # 因为overlap是两个chunk的重叠部分,必须大于0，防止丢数据，所以不能大于等于sentences_per_chunk -1
    
    # 先简单化，用正则表达式分割句子（同时支持中英文标点）
    sentences = re.split(r'(?<=[。！？；.!?])\s*', source_text) # 按句号/感叹号/问号/分号分割
    sentences = [sentence.strip() for sentence in sentences if sentence.strip() != ''] # 列表推导式，去除每个句子首位的空格，如果剩下的不是空格，保留句子

    if not sentences:
        print("没有句子块")
        return []
    
    # 处理重叠参数overlap，第一个不需要重叠，比如每个块里的句子数是3，A,B,C/C,D,E/E,F,G/这样确保有重叠
    chunks = []
    i = 0
    while i < len(sentences):
        end = min(i + sentences_per_chunk, len(sentences)) # 每一个知识块中的句子数与总的句子数比较，最多取到句子列表的末尾
        # 拼接句子块
        chunk = ' '.join(sentences[i:end]) # 把句子分成知识块，

        if overlap > 0 and i > 1: # 跳过第0块，第0块不需要重叠
            overlap_start = max(0, i - overlap)
            overlap_end = i
            overlap_chunk = ' '.join(sentences[overlap_start:overlap_end])
            chunk = overlap_chunk + ' ' + chunk
        chunks.append(chunk.strip())
        i += sentences_per_chunk
    return chunks
