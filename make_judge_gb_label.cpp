#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <filesystem>

int main() {
    std::string input_csv = "./data/buf/judge.csv";
    std::string output_csv = "./data/buf/judge_gb.csv";

    std::ifstream input(input_csv);
    std::ofstream output(output_csv);
    std::string line;

    // Write header to output CSV file
    std::getline(input, line);
    output << line << std::endl;

    // Process each line of the input CSV file
    while (std::getline(input, line)) {
        std::istringstream ss(line);
        std::string token;
        std::vector<std::string> tokens;

        while (std::getline(ss, token, ',')) {
            tokens.push_back(token);
        }

        // If Label is -1, change it to 0
        if (tokens[17] == "-1") {
            tokens[17] = "0";
        }

        // Write processed line to output CSV file
        output << tokens[0];
        for (int i = 1; i < tokens.size(); i++) {
            output << "," << tokens[i];
        }
        output << std::endl;
    }

    std::cout << "Converted " << input_csv << " to " << output_csv << std::endl;

    return 0;
}
