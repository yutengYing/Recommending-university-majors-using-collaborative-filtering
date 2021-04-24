# -*- coding: utf-8 -*-
import jieba
import to_markdown
import os
import re


class BookMark:
    def __init__(self, filename):
        self.filename = filename

    def get_markdown_name(self):
        position = os.path.splitext(self)
        markdown_name = position[0] + '.md'
        # print(markdown_name)
        return markdown_name

    def html_to_markdown(self):
        markdown_name = BookMark.get_markdown_name(self)
        to_markdown.main(self, markdown_name)

    def keep_title(self):
        file = BookMark.get_markdown_name(self)
        with open(file, 'r+', encoding='utf-8') as f:
            lines = f.readlines()
            titles = []
            for line in lines:
                title = str(re.findall(r'\[(.*?)\]', line))  # 保留[]里的内容即标题 (?<=\[)\S+(?=\])
                if not title == '[]':
                    titles.append(title)
                # print(titles)
            with open(file, 'w', encoding='utf-8') as f1:
                for t in titles:
                    # print(t[2: -2])
                    f1.write(t[2: -2] + '\n')

    def like_vector(self):
        filename = self.filename
        txt = open(filename, "r", encoding='utf-8').read()
        words = jieba.lcut(txt)  # 使用精确模式对文本进行分词
        counts = {}  # 通过键值对的形式存储词语及其出现的次数
        # removed_words = ['https', 'com', 'http']

        for word in words:
            if len(word) == 1:  # 单个词语不计算在内
                continue
            # elif word in removed_words:
            #     continue
            else:
                counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1

        items = list(counts.items())
        items.sort(key=lambda x: x[1], reverse=True)  # 根据词语出现的次数进行从大到小排序

        print(items[0:30])
        # for i in range(20):
        # word, count = items[i]
        # print("{0:<5}{1:>5}".format(word, count))

        return items[0:20]


def like_distance(bookmark_file_name1, bookmark_file_name2):
    a = dict(BookMark(bookmark_file_name1).like_vector())
    b = dict(BookMark(bookmark_file_name2).like_vector())
    return like_distance_helper(a, b)


def like_distance_helper(dict1, dict2):
    if len(dict1) == 0 or len(dict2) == 0:
        return 0.0
    a = [dict1[x] for x in dict1]
    b = [dict2[x] for x in dict2]
    z = {dict1[x]: dict2[x] for x in dict1 if x in dict2}
    x = list(z.keys())
    y = list(z.values())
    # print(x)
    result1 = 0.0
    result2 = 0.0
    result3 = 0.0
    for i in range(len(x)):
        result1 += x[i] * y[i]  # sum(X*Y)
    for j in range(len(a)):
        result2 += a[j] ** 2  # sum(X*X)
        result3 += b[j] ** 2  # sum(Y*Y)
    return result1 / ((result2 * result3) ** 0.5)


if __name__ == "__main__":
    # BookMark.get_markdown_name('../resource/书签/书签地球_1618112030364.html')
    # BookMark.html_to_markdown('../resource/书签/书签地球_1618112030364.html')
    # BookMark.keep_title('../resource/书签/书签地球_1618112030364.html')
    # BookMark.html_to_markdown('../resource/书签/书签地球_1618112020822.html')
    # BookMark.keep_title('../resource/书签/书签地球_1618112020822.html')
    print(like_distance('../resource/书签/书签地球_1618112020822.md', '../resource/书签/书签地球_1618112030364.md'))
    # print(like_distance_helper({'哔哩': 2}, {'哔哩': 10}))
    # print(like_distance_helper({'哔哩': 2}, {'莉莉': 2}))
    # print(like_distance_helper({}, {'莉莉': 2}))
