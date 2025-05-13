
def is_chinese(strings):
    for _char in strings:
        if '\u4e00' <= _char <= '\u9fa5':
            return True

word_answer = open("中文版.txt", 'w', encoding='utf-8')  # 第一个“”中是文件的名字，别忘了.txt后缀，要不然会报错
with open('老人与海 The Old Man and the Sea.txt', mode="r", encoding="utf-8") as file:
    for line in file:
        if  is_chinese(line):
            print(line)
            word_answer.write("{}".format(line))  # \n是换行符，没有换行符会黏在一起


word_answer.close()  # 把文件关上