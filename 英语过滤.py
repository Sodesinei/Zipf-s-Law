import re

with open("英文版.txt", 'r', encoding='utf-8') as f:
    text = f.read().lower()  # 统一转为小写

# 定义需要过滤的词汇集合
stop_words = set()
with open("stopwords.txt", 'r', encoding='utf-8') as f:  # 停用词文件
    for line in f:
        stop_words.add(line.strip())

# 按行处理保留段落结构
filtered_lines = []
for line in text.split('\n'):
    # 分割单词和符号（增强版正则表达式）
    tokens = re.findall(r"(\b[\w'-]+\b|[\W_]+)", line)  # 包含下划线处理

    # 过滤替换逻辑
    filtered_tokens = []
    for token in tokens:
        # 判断是否是单词（排除纯符号）
        if token.isalpha() or ("'" in token) or ("-" in token):
            # 生成等长星号替换
            filtered_tokens.append('*' * len(token) if token in stop_words else token)
        else:
            # 保留非单词符号原样
            filtered_tokens.append(token)

    # 重组当前行内容（保持原始间隔）
    filtered_line = ''.join(filtered_tokens)
    filtered_lines.append(filtered_line)

# 保留原始换行格式
content = '\n'.join(filtered_lines)

with open("英文过滤版35.txt", 'w', encoding='utf-8') as word_answer:
    word_answer.write(content)