import jieba
import re
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from openpyxl import Workbook
from collections import Counter

# 配置参数
output_dir = "中文词频分析结果"  # 输出目录名称
font_path = "msyh.ttc"  # 中文字体文件路径
top_n = 20  # 显示前N个高频词

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# ======== 数据准备 ========
with open("中文版.txt", 'r', encoding='utf-8') as f:
    text = f.read()

# 文本清洗（保留有意义的内容）
content = re.sub(r'[^\u4e00-\u9fa5]', '', text)  # 只保留中文
words = [word for word in jieba.lcut(text)]  # 过滤单字

# 词频统计（保持Counter对象）
word_counter = Counter(words)


# ======== 可视化生成 ========
def shuchu_tu(counter, output_dir):
    # 生成词云
    wc = WordCloud(
        font_path=font_path,
        width=1600,
        height=1200,
        background_color="white",
        max_words=200
    ).generate_from_frequencies(counter)

    plt.figure(figsize=(15, 10))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(os.path.join(output_dir, "中文词云图.png"), dpi=300)
    plt.close()

    # 生成统计图
    top_words = counter.most_common(top_n)
    words, counts = zip(*top_words)

    plt.figure(figsize=(12, 8))
    plt.barh(words[::-1], counts[::-1])  # 倒序显示
    plt.title(f"前{top_n}高频词分布")
    plt.xlabel("出现次数")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "中文词频统计图.png"), dpi=150)
    plt.close()


# ======== 文件输出 ========
def shuchu(counter, output_dir):
    # 文本文件
    with open(os.path.join(output_dir, "中文词频统计.txt"), 'w', encoding='utf-8') as f:
        f.write("排名\t词语\t频次\n")
        for idx, (word, count) in enumerate(counter.most_common(), 1):
            f.write(f"{idx}\t{word}\t{count}\n")

    # Excel文件
    wb = Workbook()
    ws = wb.active
    ws.append(["排名", "词语", "出现次数"])
    for idx, (word, count) in enumerate(counter.most_common(), 1):
        ws.append([idx, word, count])
    wb.save(os.path.join(output_dir, "中文词频统计.xlsx"))


# ======== 执行输出 ========
if __name__ == "__main__":
    shuchu(word_counter, output_dir)
    shuchu_tu(word_counter, output_dir)

    print(f"分析结果已保存至：{os.path.abspath(output_dir)}")
    print("包含以下文件：")
    print("- 词频统计.txt\n- 词频统计.xlsx\n- 词云图.png\n- 词频统计图.png")