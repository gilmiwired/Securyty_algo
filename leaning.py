import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from time import time
import os
import psutil

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

def train_test(data_csv, judge_csv, algorithm, features=FEATURES):
    data = pd.read_csv(data_csv)
    judge = pd.read_csv(judge_csv)

    # Select only the features specified in the FEATURES list
    data = data[['Label'] + features]
    judge = judge[features]

    X = data.drop('Label', axis=1)
    y = data['Label']

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    start_time = time()
    algorithm.fit(X_train, y_train)
    y_pred = algorithm.predict(X_test)
    execution_time = time() - start_time

    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    return {
        'accuracy': accuracy,
        'execution_time': execution_time,
        'memory_usage': memory_usage,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }

# Main
data_csvs = ['./data/buf/dataset_1_sampled.csv', './data/buf/dataset_2_sampled.csv', './data/buf/dataset_3_sampled.csv', './data/buf/dataset_4_sampled.csv', './data/buf/dataset_5_sampled.csv']
judge_csv = './data/buf/judge.csv'

algorithms = [
    ('knn', KNeighborsClassifier(n_neighbors=5)),
    ('rf', RandomForestClassifier(n_estimators=100)),
    ('svm', SVC(kernel='linear')),
    ('logreg', LogisticRegression(max_iter=1000)),
]

results = []

for algorithm_name, algorithm in algorithms:
    for data_csv in data_csvs:
        result = train_test(data_csv, judge_csv, algorithm)
        data_csv_basename = os.path.basename(data_csv)
        print(f"Algorithm: {algorithm_name}, Dataset: {data_csv_basename}, Accuracy: {result['accuracy']}, Execution_Time: {result['execution_time']}, Memory_Usage: {result['memory_usage']}, Precision: {result['precision']}, Recall: {result['recall']}, F1_Score: {result['f1_score']}")
        result['algorithm'] = algorithm_name
        result['dataset'] = data_csv_basename
        results.append(result)
        # Save results to CSV
        results_df = pd.DataFrame(results)
        results_df.to_csv('result.csv', index=False)

        print("Results saved to result.csv.")
