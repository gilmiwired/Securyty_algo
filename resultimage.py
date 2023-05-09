import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSVファイルからデータを読み込む
data = pd.read_csv("result.csv")

# 各評価指標をプロットする
metrics = ["accuracy", "execution_time", "memory_usage", "f1_score"]
n_metrics = len(metrics)

# グリッド状にグラフを配置するためのサブプロットを作成
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 12))

# グラフの色をカスタマイズ
palette = sns.color_palette("husl", len(data["algorithm"].unique()))

for i, metric in enumerate(metrics):
    # グラフの位置を決定
    row, col = i // 2, i % 2
    ax = axes[row, col]
    
    # 各アルゴリズムの評価指標をプロットする
    sns.barplot(x="algorithm", y=metric, data=data, errorbar=None, palette=palette, ax=ax)
    
    # グラフのタイトルを設定
    ax.set_title(f"Comparison of {metric.capitalize()} by Algorithm")
    ax.set_ylabel(metric.capitalize())
    ax.set_xlabel("Algorithm")

    # 各評価指標のスケールを調整
    if metric == "execution_time":
        ax.set_yscale("log")
    elif metric == "memory_usage":
        ax.set_yscale("log")

# グラフを表示
plt.tight_layout()

# グラフをPNGファイルとして保存
plt.savefig("comparison_plot2.png")

# グラフを画面に表示
plt.show()
