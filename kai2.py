import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import os

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

os.makedirs("./ANOVA", exist_ok=True)

for data_csv in data_csvs:
    print(f'Processing {data_csv}...')
    df = pd.read_csv(data_csv)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)


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
    plt.savefig(f"./ANOVA/feature_importances_{os.path.basename(data_csv).replace('.csv', '')}.png")
    plt.close()

    # カイ二乗検定を行い、結果を行列として保存
    p_values = pd.DataFrame(index=categorical_features[:-1], columns=categorical_features[:-1])
    for i, feature1 in enumerate(categorical_features[:-1]):
        for feature2 in categorical_features[i+1:-1]:
            contingency_table = pd.crosstab(df[feature1], df[feature2])
            chi2, p_val, dof, expected = chi2_contingency(contingency_table)
            p_values.loc[feature1, feature2] = p_val
            p_values.loc[feature2, feature1] = p_val
            if p_val > 0.05:
                print(f'Features: {feature1} and {feature2} might be independent as their p-value is {p_val}')
    print("\nP-Value Matrix:")
    print(p_values)


    # カイ二乗検定を行い、結果を行列として保存
    p_values = pd.DataFrame(index=categorical_features[:-1], columns=categorical_features[:-1])
    for i, feature1 in enumerate(categorical_features[:-1]):
        for feature2 in categorical_features[i+1:-1]:
            contingency_table = pd.crosstab(df[feature1], df[feature2])
            chi2, p_val, dof, expected = chi2_contingency(contingency_table)
            p_values.loc[feature1, feature2] = p_val
            p_values.loc[feature2, feature1] = p_val
            if p_val > 0.05:
                print(f'Features: {feature1} and {feature2} might be independent as their p-value is {p_val}')
    print("\nP-Value Matrix:")
    print(p_values)

    # P値のCSVファイルとして出力
    p_values.to_csv(f'./ANOVA/chi_square_p_values_{os.path.basename(data_csv).replace(".csv", "")}.csv', index=True)


    # P値のヒートマップを描画
    plt.figure(figsize=(12, 10))
    sns.heatmap(p_values.astype(float), annot=True, fmt=".2g")
    plt.title(f"P-values for Chi-square tests of {os.path.basename(data_csv)}")
    plt.savefig(f"./ANOVA/chi_square_p_values_{os.path.basename(data_csv).replace('.csv', '')}.png")
    plt.close()
