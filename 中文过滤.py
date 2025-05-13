import jieba
import re

# 加载中文停用词表（需自行准备或下载）
stop_words = set()
with open("stopwords.txt", 'r', encoding='utf-8') as f:  # 停用词文件
    for line in f:
        stop_words.add(line.strip())


with open("中文版.txt", 'r', encoding='utf-8') as f:
    text = f.read()

# 按行处理保留段落结构
filtered_lines = []
for line in text.split('\n'):
    # 精准分词（启用HMM新词发现）
    words = jieba.lcut(line, cut_all=False, HMM=True)

    # 过滤替换逻辑
    filtered_tokens = []
    for word in words:
        # 判断是否是停用词（需同时检查简体繁体）
        if word.lower() in stop_words:
            filtered_tokens.append('*' * len(word))
        else:
            # 保留非停用词和标点符号
            filtered_tokens.append(word)

    # 重组当前行内容（保持原始间隔）
    filtered_line = ''.join(filtered_tokens)
    filtered_lines.append(filtered_line)

# 保留原始换行格式
content = '\n'.join(filtered_lines)

with open("中文过滤版35.txt", 'w', encoding='utf-8') as f:
    f.write(content)