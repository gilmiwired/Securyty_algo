#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <filesystem>

const std::string HEADER = "Duration,Service,Source bytes,Destination bytes,Count,Same_srv_rate,Serror_rate,Srv_serror_rate,Dst_host_count,Dst_host_srv_count,Dst_host_same_src_port_rate,Dst_host_serror_rate,Dst_host_srv_serror_rate,Flag,IDS_detection,Malware_detection,Ashula_detection,Label,Source_IP_Address,Source_Port_Number,Destination_IP_Address,Destination_Port_Number,Start_Time,Protocol\n";

void combine_txt_to_csv(const std::string &input_dir, const std::string &output_file) {
    std::ofstream output_csv(output_file);
    output_csv << HEADER;
    
    for (const auto &txt_file : std::filesystem::directory_iterator(input_dir)) {
        std::ifstream input_txt(txt_file.path());
        std::string line;
        
        while (std::getline(input_txt, line)) {
            std::replace(line.begin(), line.end(), '\t', ',');
            output_csv << line << "\n";
        }
    }
}

int main() {
    //std::vector<std::string> data_directories = {"1day", "1week", "1month", "1quarter", "half_year", "1year"};
    std::vector<std::string> data_directories = {"dataset_1","dataset_2","dataset_3","dataset_4","dataset_5"};

    for (const std::string &data_dir : data_directories) {
        std::string input_dir = "./data/buf/" + data_dir;
        std::string output_csv = "./data/buf/" + data_dir + ".csv";
        combine_txt_to_csv(input_dir, output_csv);
        std::cout << "Combined text files in " << data_dir << " into " << output_csv << std::endl;
    }

    return 0;
}