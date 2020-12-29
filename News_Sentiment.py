import os
import time
import pandas as pd
import csv
from itertools import zip_longest

tStart = time.time()  # 計時開始

file_path = '/Users/tsengyiwen/PycharmProjects/Python/Lab/News_Sentiment'
os.chdir(file_path)

# ------------------------- Load Content & Dic ----------------------------
df = pd.read_csv('期貨_filter.csv', names=['ID', 'Content'])
# df = pd.read_csv('8.-One-Month-Dataset1.csv', names=['ID', 'Title', 'Time', 'Content'])
Dic_df = pd.read_csv('Extension_Dic.csv', names=['Positive', 'Negative'])

content_list = list(df['Content'][1:])
Pos_list = list(Dic_df['Positive'][0:33])
Neg_list = list(Dic_df['Negative'])

# -------------------------- content pre-processing -----------------------------


# -------------------------- 計算正面負面詞個數 -----------------------------
pos_list = []                   # 正面詞個數列表
neg_list = []                   # 負面詞個數列表
filiter_pos_list = []
filiter_neg_list = []

for i in range(0, len(content_list)):

    pos_num = 0                         # 累計正面詞個數
    neg_num = 0                         # 累計負面詞個數
    x = []                              # temp pos
    y = []                              # temp neg

    for line in Pos_list:
        if content_list[i].find(line) != -1:
            pos_num += 1
            x.append(line)

    filiter_pos_list.append(x)
    pos_list.append(pos_num)

    for line in Neg_list:
        if content_list[i].find(line) != -1:
            neg_num += 1
            y.append(line)

    filiter_neg_list.append(y)
    neg_list.append(neg_num)

#   ------------------- score function1 -----------------------------
def scoreMethod1(posNum, negNum):
    try:
        scorea = (posNum * 1 + negNum * -1) / (posNum + negNum)
        return scorea
    except ZeroDivisionError:
        scoreb = 0
        return scoreb

#   ------------------- score  -----------------------------
score_list = []
sentiment_list = []
standardScore = 0           # 判斷正負面評分依據

for i in range(0, len(pos_list)):
    score = scoreMethod1(pos_list[i], neg_list[i])
    score_list.append(score)

    if score > standardScore:
        sentiment_list.append('正面')
    elif score < standardScore:
        sentiment_list.append('負面')
    elif score == standardScore:
        sentiment_list.append('中性')

score_dic = list(zip_longest(score_list, sentiment_list, filiter_pos_list, filiter_neg_list))

os.chdir(file_path + '/results')

with open('ScoreDic-期貨-Extension_Dic.csv', 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerow(['Score', 'Sentiment', 'POS', 'NEG'])

    for items in score_dic:
        writer.writerow(items)

tEnd = time.time()  # 計時結束
print("This program total cost %f sec" % (tEnd - tStart))
