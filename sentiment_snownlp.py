from snownlp import SnowNLP
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('white', {'font.sans-serif': ['simhei','FangSong']})

def get_sentiment_score(data_path):
    df = pd.read_csv(data_path, encoding='utf-8')
    texts = df['content'].to_list()
    scores = []
    for i in texts:
        s = SnowNLP(i)
        print(s.sentiments) # 越接近0越负面，越接近1越正面
        scores.append(s.sentiments)
    df['sentiment_score'] = scores

# get_sentiment_score(data_path="data/chat_data.csv")

def draw(data_path):    # csv中的聊天记录有时间顺序
    df = pd.read_csv(data_path, encoding='utf-8')
    send_df = df[df['isSend']==1]
    receive_df = df[df['isSend']==0]
    send_mean = send_df.groupby('newTime').mean()
    receive_mean = receive_df.groupby('newTime').mean()

    new_df = pd.DataFrame({"月份":list(send_mean.index) + list(receive_mean.index),
                           "情感得分均值":send_mean['sentiment_score'].to_list() + receive_mean['sentiment_score'].to_list(),
                           "is_send":['send']*len(send_mean)+['receive']*len(receive_mean)})
    sns.lineplot(x="月份", y="情感得分均值", hue="is_send",data=new_df)
    plt.savefig("result/情感得分随时间变化.png")
    plt.show()

draw("data/chat_data.csv")

