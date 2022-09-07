import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('white', {'font.sans-serif': ['simhei','FangSong']})

# 绘制消息平均长度随时间变化折线图（修改一下也可以变成消息数量随时间变化...)
def draw_text_length(data_path):
    df = pd.read_csv(data_path, encoding='utf-8')
    send_df = df[df['isSend']==1]
    receive_df = df[df['isSend']==0]

    send_df['text_length'] = send_df['content'].str.len()
    receive_df['text_length'] = receive_df['content'].str.len()

    send_mean = send_df.groupby('newTime').mean()
    receive_mean = receive_df.groupby('newTime').mean()

    new_df = pd.DataFrame({"月份": list(send_mean.index) + list(receive_mean.index),
                           "消息长度均值": send_mean['text_length'].to_list() + receive_mean['text_length'].to_list(),
                           "is_send": ['send'] * len(send_mean) + ['receive'] * len(receive_mean)})

    sns.lineplot(x="月份", y="消息长度均值", hue="is_send",data=new_df)
    plt.savefig("result/句子长度均值随时间变化.png")
    plt.show()

draw_text_length("data/chat_data.csv")