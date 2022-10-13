#include <iostream>

bool valid_bit_string(const std::string &str);

/**
 * @param str - a bitstring
 * @return the crc of `str`
 */
std::string get_crc(const std::string &str);

// mod2 arithmetic operations
void mod2_div(const std::string &quotient, const std::string &divisor);

int main(int argc, char *argv[]) {
    std::string input;
    for (int i = 0; i < argc; ++i) {
        std::string flag = argv[i];
        if (flag == "-c") {
            if (i+1 >= argc) {
                std::cerr <<
                    "Error: expected an input string of bits as argument to -c"
                    << std::endl;
            }
            std::string bit_str = argv[i+1];
            if (!valid_bit_string(bit_str)) {
                std::cerr <<
                    "Error: expected a valid bit string as argument to -c"
                    << std::endl;
            }
            ++i; // skip the argument to -c
        } else if (flag == "-v") {

        } else if (flag == "-f") {

        } else if (flag == "-t") {

        } else {
            std::cerr << "Error: invalid input" << std::endl;
        }
    }
}

bool valid_bit_string(const std::string &str) {
    for (int i = 0; i < str.size(); ++i) {
        if (str[i] != '0' && str[i] != '1') {
            return false;
        }
    }
    return true;
}


std::string get_crc(const std::string &str) {
    const std::string CRC = "0100001
}

std::string mod2_div(const std::string &quotient, const std::string &divisor) {
    return "TODO";
}
