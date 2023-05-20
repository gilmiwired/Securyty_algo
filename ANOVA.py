import pandas as pd
import numpy as np
import os
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

data_csvs = [
    './data/buf/dataset_1_flug.csv', 
    './data/buf/dataset_2_flug.csv', 
    './data/buf/dataset_3_flug.csv', 
    './data/buf/dataset_4_flug.csv', 
    './data/buf/dataset_5_flug.csv'
]

numeric_features = [
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
    'Source_Port_Number',
    'Destination_Port_Number',
]

categorical_features = [
    'Common_Flag',
    'Unfinished_Flag',
    'Denial_Flag',
    'Reset_Flag',
    'Other_Flag',
    'SSH_Service',
    'Other_Service',
    'DNS_Service',
    'Multiple_Other_Services',
    'TCP_Protocol',
    'UDP_Protocol',
    'Other_Protocol',
    'Label',
]

for data_csv in data_csvs:
    print(f'Processing {data_csv}...')
    df = pd.read_csv(data_csv)

    # ANOVAの計算
    for feature in numeric_features:
        groups = df.groupby('Label')[feature].apply(list)
        f_val, p_val = stats.f_oneway(*groups)
        print(f'Feature: {feature}, F-value: {f_val}, p-value: {p_val}')

    # ランダムフォレストによるRMSEの計算
    X = df[numeric_features + categorical_features[:-1]]  # Labelは目的変数なので除外
    y = df['Label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f'RMSE: {rmse}')

    # 特徴量重要度のプロット
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]

    plt.figure(figsize=(12,6))
    plt.title(f"Feature importances for {data_csv}")
    plt.bar(range(X.shape[1]), importances[indices], color="r", align="center")
    plt.xticks(range(X.shape[1]), [X.columns[i] for i in indices], rotation='vertical')
    plt.xlim([-1, X.shape[1]])
    plt.show()

    # 相関行列の計算
    corr_matrix = X.corr()

    # 相関行列をコマンドラインに出力
    print(corr_matrix)
    # 相関行列のヒートマップの作成と保存
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    file_name = os.path.basename(data_csv).replace('.csv', '')  # CSVファイルの名前を取得
    plt.savefig(f'corr_matrix_{file_name}.png')
    plt.close()  # プロットを表示せずに閉じる
