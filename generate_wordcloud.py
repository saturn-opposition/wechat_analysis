from wordcloud import WordCloud
import pandas as pd
import jieba
import re
from collections import Counter
import matplotlib.pyplot as plt

def get_wordcloud(data_path,save_path,is_send=0):
    '''

    :param data_path: 聊天记录文件csv
    :param is_send: 0代表对方发送的消息，1代表我发送的消息
    :param save_path: 词云保存路径
    :return:
    '''

    df = pd.read_csv(data_path,encoding='utf-8')
    texts = df[df['isSend']==is_send]['content'].to_list()

    with open("data/CNstopwords.txt",'r',encoding='utf-8') as f:
        lines = f.readlines()
        stopwords = [line.strip().replace("\ufeff","") for line in lines]

    # 分词，去除停用词和表情（表情都是这样的格式：[xx]）
    norm_texts = []
    pattern = re.compile("(\[.+?\])")
    for text in texts:
        text = pattern.sub('', text).replace("\n","")    # 删除表情、换行符
        words = jieba.lcut(text)
        res = [word for word in words if word not in stopwords and word.replace(" ","")!="" and len(word)>1]
        if res!=[]:
            norm_texts.extend(res)

    count_dict = dict(Counter(norm_texts))
    wc = WordCloud(font_path="data/simhei.ttf", background_color='white', include_numbers=False,
                   random_state=0)      # 如果不指定中文字体路径，词云会乱码
    wc = wc.fit_words(count_dict)
    plt.imshow(wc)
    plt.show()
    wc.to_file(save_path)

# 示例：绘制 对方 发送的信息的词云图
get_wordcloud("data/chat_data.csv",save_path="result/词云-他发的.png",is_send=0)
