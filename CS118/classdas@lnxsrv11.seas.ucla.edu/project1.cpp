// Nima Amir Dastmalchi
// 505320372

#include "Bitstream.h"

#include <iostream>
#include <vector>

bool valid_bit_string(const std::string &str);
Bitstream get_message_plus_crc(const std::string &bit_str, const Bitstream &generator);

int main(int argc, char *argv[]) {
    // expecting 2 extra arguments:
    if (argc < 3) {
        return 0;
    }
    std::string input;
    std::string flag = argv[1];
    if (flag != "-c" && flag != "-v" && flag != "-f" && flag != "-t" && flag != "-p") {
        std::cerr << "Error: Unexpected flag " << flag << std::endl;
        return 1;
    }
    std::string bit_str = argv[2];
    if (!valid_bit_string(bit_str)) {
        std::cerr <<
            "Error: expected a valid bit string as argument to -c" << std::endl;
        return 1;
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
        for (int i = num_bits-1; i >= 3; --i) {
            for (int j = i-1; j >= 2; --j) {
                for (int k = j-1; k >= 1; --k) {
                    for (int l = k-1; l >= 0; --l) {
                        int error_bits[] = {i, j, k, l};
                        Bitstream error(error_bits, 4);
                        Bitstream result = add(data_plus_crc, std::move(error));
                        result.set_min_size(data_plus_crc.num_bits());
                        if (get_remainder(result, generator).is_zero()) {
                            std::cout << result.to_string() << std::endl;
                        }
                    }
                }
            }
        }
    } else if (flag == "-t") {
        // Create the generator
        int generator_bits[] = {16, 15, 12, 2, 0};
        int num_generator_bits = generator_bits[0] + 1; // assuming bits is sorted 
        Bitstream generator(generator_bits,
                            sizeof(generator_bits) / sizeof(generator_bits[0]));
        // Compute data + crc
        Bitstream data_plus_crc = get_message_plus_crc(bit_str, generator);
        int num_bits = data_plus_crc.num_bits();           

        // Find all undetected 5 bit errors:
        int num_five_bit_errors = 0;
        for (int i = num_bits-1; i >= 4; --i) {
            for (int j = i-1; j >= 3; --j) {
                for (int k = j-1; k >= 2; --k) {
                    for (int l = k-1; l >= 1; --l) {
                        for (int m = l-1; m >= 0; --m) {
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
    } else if (flag == "-p") {
        // The generator is x^16 + x^15 + x^2 + 1, which is divisible by x + 1.
        // Therefore, all odd-bit errors will be detected. So, we can just ouput
        // 0 without looking at the input.
        std::cout << 0 << std::endl;
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
    data.set_min_size(bit_str.size() + generator.num_bits() - 1);
    return std::move(data);
}
