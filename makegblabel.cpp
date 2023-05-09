#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

const std::string HEADER = "Duration,Service,Source bytes,Destination bytes,Count,Same_srv_rate,Serror_rate,Srv_serror_rate,Dst_host_count,Dst_host_srv_count,Dst_host_same_src_port_rate,Dst_host_serror_rate,Dst_host_srv_serror_rate,Flag,IDS_detection,Malware_detection,Ashula_detection,Label,Source_IP_Address,Source_Port_Number,Destination_IP_Address,Destination_Port_Number,Start_Time,Protocol\n";

void convert_label_to_0(const std::string& input_csv, const std::string& output_csv) {
    std::ifstream input(input_csv);
    std::ofstream output(output_csv);
    std::string line;

    // Read input CSV file and convert -1 labels to 0
    std::getline(input, line); // Skip header
    output << line << "\n"; // Write header
    while (std::getline(input, line)) {
        std::istringstream ss(line);
        std::string token;
        std::vector<std::string> tokens;

        while (std::getline(ss, token, ',')) {
            tokens.push_back(token);
        }

        if (tokens[17] == "-1") {
            tokens[17] = "0";
            line = tokens[0];
            for (int i = 1; i < tokens.size(); i++) {
                line += "," + tokens[i];
            }
        }

        output << line << "\n";
    }
}

int main() {
    std::vector<std::string> input_csvs = {"dataset_1_sampled.csv", "dataset_2_sampled.csv", "dataset_3_sampled.csv", "dataset_4_sampled.csv", "dataset_5_sampled.csv"};

    for (const std::string& input_csv : input_csvs) {
        std::string output_csv = "./data/buf/" + input_csv.substr(0, input_csv.find(".")) + "_gb_sampled.csv";

        convert_label_to_0("./data/buf/" + input_csv, output_csv);

        std::cout << "Converted -1 labels to 0 in " << input_csv << " and saved to " << output_csv << std::endl;
    }

    return 0;
}
