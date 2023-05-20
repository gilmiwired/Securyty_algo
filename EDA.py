#EDA元データセットに対して行う要
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

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

    'Source_Port_Number',
    'Destination_Port_Number',

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

CATEGORICAL_FEATURES = ['Flag', 'Service', 'Protocol']

def eda_and_categorical_counts(file_name, features, categorical_features):
    df = pd.read_csv(file_name, dtype={feature: str for feature in categorical_features})
    df = df[features + categorical_features]  # Include categorical features

    print(f"=== Basic statistics for {file_name} ===")
    print(df.describe())

    print(f"\n=== Histograms for {file_name} ===")
    df.hist(bins=50, figsize=(20,15))
    plt.tight_layout()
    plt.savefig(f"images/{file_name.split('/')[-1].replace('.csv', '_dispersion.png')}")
    plt.close()

    print(f"\n=== Correlation matrix for {file_name} ===")
    numeric_df = df.select_dtypes(include=['float64', 'int64'])  # Select only numeric features for correlation
    corr_matrix = numeric_df.corr()
    print(corr_matrix)

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title(f"Correlation Matrix for {file_name}")
    plt.savefig(f"images/{file_name.split('/')[-1].replace('.csv', '_correlation.png')}")
    plt.close()

    print(f"\n=== Value counts for categorical features in {file_name} ===")
    for feature in categorical_features:
        print(df[feature].value_counts())

        # Add bar plot for each categorical feature
        print(f"\n=== Bar plot for feature {feature} in {file_name} ===")
        value_counts = df[feature].value_counts()
        plt.figure(figsize=(10, 6))
        plt.bar(value_counts.index, value_counts.values)
        plt.title(f"Bar plot for feature {feature}")
        plt.ylabel('Count')
        plt.xticks(rotation=90)  # Rotate x labels for better visibility if there are many categories
        plt.tight_layout()
        plt.savefig(f"images/{file_name.split('/')[-1].replace('.csv', f'_{feature}_barplot.png')}")
        plt.close()

# Main
os.makedirs("images", exist_ok=True)
#data_csvs = ['./data/buf/dataset_1.csv', './data/buf/dataset_2.csv', './data/buf/dataset_3.csv', './data/buf/dataset_4.csv', './data/buf/dataset_5.csv']
data_csvs = ['./data/buf/dataset_1_flug.csv', './data/buf/dataset_2_flug.csv', './data/buf/dataset_3_flug.csv', './data/buf/dataset_4_flug.csv', './data/buf/dataset_5_flug.csv']


for data_csv in data_csvs:
    eda_and_categorical_counts(data_csv, FEATURES, CATEGORICAL_FEATURES)
