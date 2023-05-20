import os
import glob
import pandas as pd
import csv

HEADER = [
    "Duration",
    "Service",
    "Source bytes",
    "Destination bytes",
    "Count",
    "Same_srv_rate",
    "Serror_rate",
    "Srv_serror_rate",
    "Dst_host_count",
    "Dst_host_srv_count",
    "Dst_host_same_src_port_rate",
    "Dst_host_serror_rate",
    "Dst_host_srv_serror_rate",
    "Flag",
    "IDS_detection",
    "Malware_detection",
    "Ashula_detection",
    "Label",
    "Source_IP_Address",
    "Source_Port_Number",
    "Destination_IP_Address",
    "Destination_Port_Number",
    "Start_Time",
    "Protocol"
]

def combine_txt_to_csv(txt_files, csv_path):
    combined_data = [HEADER]
    for txt_file in txt_files:
        with open(txt_file, "r") as f:
            data = [row for row in csv.reader(f, delimiter="\t")]
        combined_data.extend(data)

    df = pd.DataFrame(combined_data[1:], columns=HEADER)
    df.to_csv(csv_path, index=False)

if __name__ == "__main__":
    
    data_directories = ["1day", "1week", "1month", "1quarter", "half_year", "1year"]

    for data_dir in data_directories:
        txt_files = glob.glob(f"./data/buf/{data_dir}/*.txt")
        csv_path = f"./data/buf/{data_dir}.csv"

        combine_txt_to_csv(txt_files, csv_path)
        print(f"Combined text files in {data_dir} into {csv_path}")
