import re
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from openpyxl import Workbook
from collections import Counter

# 配置参数
output_dir = "英文版词频统计"  # 输出目录名称
top_n = 20  # 显示前N个高频词
width, height = 1600, 1200  # 词云图尺寸

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# ======== 数据准备 ========
with open("英文版.txt", 'r', encoding='utf-8') as f:  # 输入文件名称
    text = f.read().lower()  # 统一转为小写

# 文本处理（保留连字符和缩写）
words = re.findall(r"\b[\w'-]+\b", text)  # 匹配英文单词（包含连字符和所有格）

# 词频统计
word_counter = Counter(words)


# ======== 可视化生成 ========
def generate_visualizations(counter, output_dir):
    # 生成词云
    wc = WordCloud(
        width=width,
        height=height,
        background_color="white",
        collocations=False,  # 禁用词组搭配
        max_words=200
    ).generate_from_frequencies(counter)

    plt.figure(figsize=(15, 10))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(os.path.join(output_dir, "英文词云图.png"), dpi=300)
    plt.close()

    # 生成统计图
    top_words = counter.most_common(top_n)
    words, counts = zip(*top_words)

    plt.figure(figsize=(12, 8))
    plt.barh(words[::-1], counts[::-1])
    plt.title(f"Top {top_n} Frequent Words")
    plt.xlabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "英文词频图.png"), dpi=150)
    plt.close()


# ======== 文件输出 ========
def export_files(counter, output_dir):
    # 文本文件
    with open(os.path.join(output_dir, "英文词频统计结果.txt"), 'w', encoding='utf-8') as f:
        f.write("Rank\tWord\tFrequency\n")
        for idx, (word, count) in enumerate(counter.most_common(), 1):
            f.write(f"{idx}\t{word}\t{count}\n")

    # Excel文件
    wb = Workbook()
    ws = wb.active
    ws.append(["Rank", "Word", "Count"])
    for idx, (word, count) in enumerate(counter.most_common(), 1):
        ws.append([idx, word, count])
    wb.save(os.path.join(output_dir, "英文词频统计结果.xlsx"))


# ======== 执行输出 ========
if __name__ == "__main__":
    export_files(word_counter, output_dir)
    generate_visualizations(word_counter, output_dir)

    print(f"Results saved to: {os.path.abspath(output_dir)}")
    print("Contains:")
    print("- 英文词频统计结果.txt\n- 英文词频统计结果.xlsx\n- 英文词云图.png\n- 英文词频图.png")