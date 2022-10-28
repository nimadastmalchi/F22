#include "Bitstream.h"

#include <iostream>
#include <vector>

bool valid_bit_string(const std::string &str);
Bitstream get_message_plus_crc(const std::string &bit_str, const Bitstream &generator);

int main(int argc, char *argv[]) {
    if (argc <= 1) {
        return 0;
    }
    std::string input;
    for (int i = 1; i < argc; i+=2) {
        std::string flag = argv[i];
        if (flag != "-c" && flag != "-v" && flag != "-f" && flag != "-t" && flag != "-p") {
            std::cerr <<
                "Error: Unexpected flag " << flag << std::endl;
            continue;
        }
        if (i+1 >= argc) {
            std::cerr <<
                "Error: expected an input string of bits as argument to " << flag
                << std::endl;
            continue;
        }
        std::string bit_str = argv[i+1];
        if (!valid_bit_string(bit_str)) {
            std::cerr <<
                "Error: expected a valid bit string as argument to -c"
                << std::endl;
            continue;
        }
        if (flag == "-c") {
            // Create the generator:
            int generator_bits[] = {16, 12, 7, 5, 0};
            int num_generator_bits = generator_bits[0] + 1; // assuming bits is sorted 
            Bitstream generator(generator_bits,
                                sizeof(generator_bits) / sizeof(generator_bits[0]));

            // Compute the data + CRC:
            Bitstream data_plus_crc = get_message_plus_crc(bit_str, generator);
            std::cout << data_plus_crc.to_string() << std::endl;
        } else if (flag == "-v") {
            // Create the generator:
            int generator_bits[] = {16, 12, 7, 5, 0};
            int num_generator_bits = generator_bits[0] + 1; // assuming bits is sorted 
            Bitstream generator(generator_bits,
                                sizeof(generator_bits) / sizeof(generator_bits[0]));
            // Divide data by generator and examine the remainder:
            Bitstream data(bit_str);
            if (get_remainder(data, generator).is_zero()) {
                std::cout << "1" << std::endl;
            } else {
                std::cout << "0" << std::endl;
            }
        } else if (flag == "-f") {
            // Create the generator
            int generator_bits[] = {16, 15, 12, 2, 0};
            int num_generator_bits = generator_bits[0] + 1; // assuming bits is sorted 
            Bitstream generator(generator_bits,
                                sizeof(generator_bits) / sizeof(generator_bits[0]));
            // Compute data + crc
            Bitstream data_plus_crc = get_message_plus_crc(bit_str, generator);
            int num_bits = data_plus_crc.num_bits();           

            // Find all undetected 4 bit errors:
            for (int i = 0; i < num_bits; ++i) {
                for (int j = i + 1; j < num_bits; ++j) {
                    for (int k = j + 1; k < num_bits; ++k) {
                        for (int l = k + 1; l < num_bits; ++l) {
                            int error_bits[] = {i, j, k, l};
                            Bitstream error(error_bits, 4);
                            Bitstream result = add(data_plus_crc, std::move(error));
                            if (get_remainder(result, generator).is_zero()) {
                                std::cout << result.to_string() << std::endl;
                            }
                        }
                    }
                }
            }
        } else if (flag == "-t" || flag == "-p") {
            // Create the generator
            Bitstream generator;
            if (flag == "-t") {
                int generator_bits[] = {16, 15, 12, 2, 0};
                int num_generator_bits = generator_bits[0] + 1; // assuming bits is sorted 
                generator = Bitstream(generator_bits,
                                      sizeof(generator_bits) / sizeof(generator_bits[0]));
            } else {
                int generator_bits[] = {16, 15, 2, 0};
                int num_generator_bits = generator_bits[0] + 1; // assuming bits is sorted 
                generator = Bitstream(generator_bits,
                                      sizeof(generator_bits) / sizeof(generator_bits[0]));
            }
            // Compute data + crc
            Bitstream data_plus_crc = get_message_plus_crc(bit_str, generator);
            int num_bits = data_plus_crc.num_bits();           

            // Find all undetected 5 bit errors:
            int num_five_bit_errors = 0;
            for (int i = 0; i < num_bits; ++i) {
                for (int j = i + 1; j < num_bits; ++j) {
                    for (int k = j + 1; k < num_bits; ++k) {
                        for (int l = k + 1; l < num_bits; ++l) {
                            for (int m = l + 1; m < num_bits; ++m) {
                                int error_bits[] = {i, j, k, l, m};
                                Bitstream error(error_bits, 5);
                                Bitstream result = add(data_plus_crc, std::move(error));
                                if (get_remainder(result, generator).is_zero()) {
                                    ++num_five_bit_errors;
                                }
                            }
                        }
                    }
                }
            }
            std::cout << num_five_bit_errors << std::endl;
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

Bitstream get_message_plus_crc(const std::string &bit_str, const Bitstream &generator) {
    Bitstream data(bit_str);
    data = data.single_mult(generator.num_bits() - 1);
    Bitstream crc = get_remainder(data, generator);
    data.add(std::move(crc));
    return std::move(data);
}
