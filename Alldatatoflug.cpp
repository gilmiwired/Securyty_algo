#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>

using namespace std;

const string HEADER = "Duration,Service,Source bytes,Destination bytes,Count,Same_srv_rate,Serror_rate,Srv_serror_rate,Dst_host_count,Dst_host_srv_count,Dst_host_same_src_port_rate,Dst_host_serror_rate,Dst_host_srv_serror_rate,Flag,IDS_detection,Malware_detection,Ashula_detection,Label,Source_IP_Address,Source_Port_Number,Destination_IP_Address,Destination_Port_Number,Start_Time,Protocol,Common_Flag,Unfinished_Flag,Denial_Flag,Reset_Flag,Other_Flag,SSH_Service,Other_Service,DNS_Service,Multiple_Other_Services,TCP_Protocol,UDP_Protocol,Other_Protocol\n";

void convert_label_to_0_and_add_features(const string& input_csv, const string& output_csv) {
    ifstream input(input_csv);
    ofstream output(output_csv);
    string line;

    getline(input, line); // Skip header
    output << HEADER; // Write extended header

    while (getline(input, line)) {
        istringstream ss(line);
        string token;
        vector<string> tokens;

        while (getline(ss, token, ',')) {
            tokens.push_back(token);
        }

        tokens[17] = (tokens[17] == "-1") ? "0" : tokens[17];

        // Add new features
        tokens.push_back((tokens[13] == "SF") ? "1" : "0"); // Common_Flag
        tokens.push_back((tokens[13] == "S0" || tokens[13] == "S1" || tokens[13] == "S2" || tokens[13] == "S3" || tokens[13] == "SH" || tokens[13] == "SHR") ? "1" : "0"); // Unfinished_Flag
        tokens.push_back((tokens[13] == "REJ" || tokens[13] == "RSTRH") ? "1" : "0"); // Denial_Flag
        tokens.push_back((tokens[13] == "RSTO" || tokens[13] == "RSTR" || tokens[13] == "RSTOS0") ? "1" : "0"); // Reset_Flag
        tokens.push_back((tokens[13] == "OTH") ? "1" : "0"); // Other_Flag

        // Add new service features
        tokens.push_back((tokens[1] == "ssh") ? "1" : "0"); // SSH_Service
        tokens.push_back((tokens[1] == "other") ? "1" : "0"); // Other_Service
        tokens.push_back((tokens[1] == "dns") ? "1" : "0"); // DNS_Service
        tokens.push_back((tokens[1] != "ssh" && tokens[1] != "other" && tokens[1] != "dns") ? "1" : "0"); // "Multiple_Other_Services"

        tokens.push_back((tokens[24] == "tcp") ? "1" : "0"); // TCP_Protocol
        tokens.push_back((tokens[24] == "udp") ? "1" : "0"); // UDP_Protocol
        tokens.push_back((tokens[24] != "tcp" && tokens[24] != "udp") ? "1" : "0"); // Other_Protocol

        // Write processed line to output CSV file
        output << tokens[0];
        for (int i = 1; i < tokens.size(); i++) {
            output << "," << tokens[i];
        }
        output << "\n";
    }
}


int main() {
    vector<string> data_csvs = {"dataset_1", "dataset_2", "dataset_3", "dataset_4", "dataset_5"};

    for (const string& data_csv : data_csvs) {
        string input_csv = "./data/buf/" + data_csv + ".csv";
        string output_csv = "./data/buf/" + data_csv + "_flug.csv";

        convert_label_to_0_and_add_features(input_csv, output_csv);

        cout << "Converted -1 and -2 labels to 0 and added new features in " << input_csv << " and saved to " << output_csv << endl;
    }

    return 0;
}
