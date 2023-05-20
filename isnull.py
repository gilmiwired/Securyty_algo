import pandas as pd
import os

# データセットのディレクトリ名
datasets = ["dataset_1","dataset_2","dataset_3","dataset_4","dataset_5"]

# 各データセットに対して欠損値の確認を行う
for dataset in datasets:
    # ファイルパスを作成
    file_path = os.path.join("data", "buf", dataset + ".csv")
    
    # CSVファイルを読み込む
    df = pd.read_csv(file_path)
    
    # 各列の欠損値の数を取得する
    missing_values = df.isnull().sum()
    
    # データセット名と欠損値の数を表示する
    print(f"\n{dataset}:\n")
    print(missing_values)
