#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <filesystem>
#include <algorithm>
#include <ctime>
#include <cstdlib>
#include <random>

const std::string HEADER = "Duration,Service,Source bytes,Destination bytes,Count,Same_srv_rate,Serror_rate,Srv_serror_rate,Dst_host_count,Dst_host_srv_count,Dst_host_same_src_port_rate,Dst_host_serror_rate,Dst_host_srv_serror_rate,Flag,IDS_detection,Malware_detection,Ashula_detection,Label,Source_IP_Address,Source_Port_Number,Destination_IP_Address,Destination_Port_Number,Start_Time,Protocol\n";

void extract_data_from_csv(const std::string& input_csv, const std::string& output_csv, int num_positives, int num_negatives) {
    std::ifstream input(input_csv);
    std::ofstream output(output_csv);
    std::string line;
    std::vector<std::string> positive_data, negative_data;

    // Read input CSV file and extract positive and negative data
    std::getline(input, line); // Skip header
    while (std::getline(input, line)) {
        std::istringstream ss(line);
        std::string token;
        std::vector<std::string> tokens;

        while (std::getline(ss, token, ',')) {
            tokens.push_back(token);
        }

        if (tokens[17] == "1") {
            positive_data.push_back(line);
        } else if (tokens[17] == "-1") {
            negative_data.push_back(line);
        }
    }

    // Check if there is enough data
    if (positive_data.size() < num_positives || negative_data.size() < num_negatives) {
        std::cerr << "Not enough data to sample " << num_positives << " positives and " << num_negatives << " negatives." << std::endl;
        return;
    }

    // Shuffle data
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(positive_data.begin(), positive_data.end(), g);
    std::shuffle(negative_data.begin(), negative_data.end(), g);

    // Write output CSV file
    output << HEADER;
    for (int i = 0; i < num_positives; i++) {
        output << positive_data[i] << "\n";
    }
    for (int i = 0; i < num_negatives; i++) {
        output << negative_data[i] << "\n";
    }
}

int main() {
    std::vector<std::string> data_csvs = {"dataset_1.csv", "dataset_2.csv", "dataset_3.csv", "dataset_4.csv", "dataset_5.csv"};

    for (const std::string& data_csv : data_csvs) {
        std::string input_csv = "./data/buf/" + data_csv;
        std::string output_csv = "./data/buf/" + data_csv.substr(0, data_csv.find(".")) + "_sampled.csv";

        extract_data_from_csv(input_csv, output_csv, 1000, 1000);

        std::cout << "Extracted 1000 positive and 1000 negative samples from " << input_csv << " to " << output_csv << std::endl;
    }

    return 0;
}
