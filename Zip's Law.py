import os
import math
import jieba
import jieba.analyse
import logging
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.sans-serif'] = [u'SimHei']  # 中文字体可修改
mpl.rcParams['axes.unicode_minus'] = False

class jyxstxtqj_downcc:
    def __init__(self, name):
        self.data = None
        self.name = name
        # 单个字
        self.word = []  # 单个字列表
        self.word_len = 0  # 单个字总字数

        with open("cn_punctuation.txt", "r", encoding='utf-8') as f:
            self.punc_word = f.read().split('\n')
            f.close()

    def read_file(self, filename=""):
        # 如果未指定名称，则默认为类名
        if filename == "":
            filename = self.name
        target = "jyxstxtqj_downcc.com/" + filename + ".txt"
        with open(target, "r", encoding='gbk', errors='ignore') as f:
            self.data = f.read()
            self.data = self.data.replace(
                '本书来自www.cr173.com免费txt小说下载站\n更多更新免费电子书请关注www.cr173.com', '')
            f.close()


    def write_file(self):
        # 将文件内容写入总文件
        target = "jyxstxtqj_downcc.com/data0.txt"
        with open(target, "a") as f:
            f.write(self.data)
            f.close()

if __name__ == "__main__":
    data_set_list = []
    # 每次运行程序将总内容文件清空
    with open("jyxstxtqj_downcc.com/data0.txt", "w") as f:
        f.close()

    # 读取小说名字
    with open("jyxstxtqj_downcc.com/inf.txt", "r") as f:
        txt_list = f.read().split(',')
        i = 0
        for name in txt_list:
            locals()[f'set{i}'] = jyxstxtqj_downcc(name)
            data_set_list.append(locals()[f'set{i}'])
            i += 1
        f.close()

    
    for set in data_set_list:
        set.read_file()
        set.write_file()

    data0 = open("jyxstxtqj_downcc.com/data0.txt", "r", encoding="gb18030").read()
    
    punc_word = open("cn_punctuation.txt", "r", encoding='utf-8').read()

    #语法表的添加与删除
    punc_word = punc_word.split('\n')
    punc_word += '\u3000'
    punc_word += '\n'
    punc_word.remove('⑩')
    punc_word.remove('﹏')
    punc_word.remove('|')

    
    #利用jieba分词
    words = jieba.lcut(data0)

    #设置初始字典
    counts = {}

    #开始遍历计数
    for word in words:
        counts[word] = counts.get(word,0)+1


    #print(punc_word)
    #print("out")
    #print(counts['\n'])

    
    #去除标点符号
    for word in punc_word:
        del counts[word]


       
    #返回遍历得分所有键与值
    items = list(counts.items())
    print(len(items))

    #根据词出现次序进行排序
    items.sort(key=lambda x: x[1], reverse=True)
    #sort_list用于绘图时的数据列表
    sort_list = sorted(counts.values(), reverse=True)

    #将数据写入txt文本
    file = open('word_fre.txt', mode='w',encoding='utf-8')

    #输出词语与词频
    for i in range(159747):
        word, count = items[i]
        #print("{0:<10}{1:>5}".format(word,count))

        #写入txt文件
        new_context = word + "   " + str(count) + '\n'
        file.write(new_context)

    file.close()
    
    #用matplotlib验证Zipf-Law
    plt.title('Zipf-Law',fontsize=18)
    plt.xlabel('rank',fontsize=18)  #排名
    plt.ylabel('freq',fontsize=18) #频度
    plt.yticks([pow(10,i) for i in range(0,4)])  # 设置y刻度
    plt.xticks([pow(10,i) for i in range(0,4)])  # 设置x刻度
    x = [i for i in range(len(sort_list))]
    plt.yscale('log')#设置纵坐标的缩放
    plt.xscale('log')
    plt.plot(x, sort_list , 'r')
    plt.savefig('./Zipf_Law.jpg')
    plt.show()







    
