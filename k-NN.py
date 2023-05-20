from __future__ import print_function
import sys
import time
import pandas as pd
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
import os
import psutil
import csv

TRAIN_FILENAMES = [
    "1day.csv",
    "3day.csv",
    "5day.csv",
    "1week.csv",
    "2week.csv",
    "1month.csv",
    "1quarter.csv",
    "half_year.csv",
    "1year.csv",
]

TEST_FILENAME = "judge.csv"
TRAIN_DIR = "./data/buf/"
TEST_PATH = os.path.join(TRAIN_DIR, TEST_FILENAME)

N = 10000
LABEL_NORMAL = 1
LABEL_ATTACK = -1

FEATURES = [
    'Duration',  
    'Source bytes',
    'Destination bytes',
    'Count',
    'Same_srv_rate',
    'Serror_rate',
    'Srv_serror_rate',
    'Dst_host_count',
    'Dst_host_srv_count',
    'Dst_host_same_src_port_rate',
    'Dst_host_serror_rate',
    'Dst_host_srv_serror_rate',
]

def read_dataset(path, n=N):
    df = pd.read_csv(path,encoding="utf-8",on_bad_lines="skip")
    # データフレームのうちラベルが正常のもの
    normal = df[df.Label == LABEL_NORMAL]
    # 正常なものについて使用する特徴量のみを切り出してサンプリング
    normal = normal.loc[:, FEATURES].sample(n)

    # データフレームのうちラベルが攻撃のもの
    attack = df[df.Label == LABEL_ATTACK]
    # 攻撃について使用する特徴量のみを切り出してサンプリング
    # クラスごとのサンプル数が不均衡なのは望ましくないので同数にします
    attack = attack.loc[:, FEATURES].sample(n)

    label = [LABEL_NORMAL] * len(normal) + [LABEL_ATTACK] * len(attack)
    print('正常 : {}, 攻撃 : {}'.format(normal.shape, attack.shape))

    return pd.concat((normal, attack)), label

def main():
    process = psutil.Process(os.getpid())
    
    test, label_test = read_dataset(TEST_PATH)
    
    for train_filename in TRAIN_FILENAMES:
        print(f"Using {train_filename} for training")
        start_time = time.time()
        
        train_path = os.path.join(TRAIN_DIR, train_filename)
        train, label_train = read_dataset(train_path)
        
        clf = KNeighborsClassifier()
        clf.fit(train, label_train)
        
        pred = clf.predict(test)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        mem_info = process.memory_info()
        
        accuracy = metrics.accuracy_score(pred, label_test) * 100
        precision = metrics.precision_score(pred, label_test)
        recall = metrics.recall_score(pred, label_test)
        f1 = metrics.f1_score(pred, label_test)
        
        print(f"Algorithm: KNeighborsClassifier")
        print(f"Training data: {train_filename}")
        print(f"Accuracy: {accuracy:.2f}%")
        print(f"Execution time: {elapsed_time:.2f} seconds")
        print(f"Memory usage: {mem_info.rss / (1024 ** 2)} MB")
        print(f"Precision: {precision:.2f}")
        print(f"Recall: {recall:.2f}")
        print(f"F1 score: {f1:.2f}")
        print("\n")
        file_exists = os.path.isfile('result.csv')
        with open('result.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            accuracy = metrics.accuracy_score(pred, label_test) * 100

            # ファイルが存在しなかった場合、ヘッダーを書き込む
            if not file_exists:
                writer.writerow(['accuracy'])

            writer.writerow([accuracy])

        print('正解率 : {:.2f} %'.format(accuracy))


if __name__ == '__main__':
        main()
