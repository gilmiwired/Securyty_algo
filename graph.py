import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# CSVファイルからデータを読み込む
data = pd.read_csv("aditional_result.csv")

# カラー設定
colors = ['k', 'r', 'b', 'y', 'm']

# データセットと色のマッピング
color_dict = {}
for dataset_name in data['dataset'].unique():
    dataset_index = int(dataset_name.split('_')[1]) - 1  # dataset_1, dataset_2, etc.からインデックスを取得
    color_dict[dataset_name] = colors[dataset_index % len(colors)]  # データセット数が色の数を超えた場合に備えてmod演算を行います

def plot_status(algorithm_name, metric):
    plt.figure(figsize=(10, 6))
    # アルゴリズムに関連するデータを抽出
    algorithm_data = data[data["algorithm"] == algorithm_name]

    # データセットごとに
    for dataset_name in np.sort(algorithm_data["dataset"].unique()):
        # データセットに関連するデータを抽出
        dataset_data = algorithm_data[algorithm_data["dataset"] == dataset_name]
        # プロット
        plt.plot(dataset_data[metric], color=color_dict[dataset_name], marker='o')

    # グラフのタイトルと軸ラベルを設定
    plt.title(f"{algorithm_name} {metric.capitalize()} over Datasets")
    plt.ylabel(metric.capitalize())
    plt.xlabel("Dataset")
    plt.gca().xaxis.set_major_locator(plt.NullLocator())  # x軸のラベルを削除

    # 凡例を表示
    for dataset_name, color in zip(['dataset_1', 'dataset_2', 'dataset_3', 'dataset_4', 'dataset_5'], colors):
        plt.plot([], [], color=color, label=dataset_name)
    plt.legend(loc='lower right')

    # ディレクトリを作成
    directory = f"{algorithm_name}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # グラフをPNGファイルとして保存
    plt.savefig(f"{directory}/{algorithm_name}_{metric}.png")

    # グラフの表示をクリア
    plt.clf()

# アルゴリズムと評価指標のリスト
algorithms = ['knn', 'rf', 'svm', 'logreg', 'dt', 'gb', 'xgb', 'lgbm', 'nb', 'mlp', 'ada', 'bag', 'et', 'logit', 'svm_prob', 'linearSVC', 'tree']
metrics = ['accuracy', 'execution_time', 'memory_usage', 'f1_score']

# 各アルゴリズムと評価指標に対してプロットを生成
for algorithm in algorithms:
    for metric in metrics:
        plot_status(algorithm, metric)