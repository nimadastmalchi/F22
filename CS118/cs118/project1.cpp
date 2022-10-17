#include <algorithm>
#include <iostream>
#include <vector>
#include <unordered_set>

// Represents a bitstream
class Bitstream {
public:
    Bitstream(const std::string &bitstream="") {
        for (int i = 0; i < bitstream.size(); ++i) {
            if (bitstream[i] == '1') {
                this->bits.insert(i);
            }
        }
    }

    void add(const Bitstream &other) {
        // For all elements elem of other, if there elem is in this, then remove
        // it. Otherwise, add it (i.e., compute xor).
        for (const auto &elem : other.bits) {
            if (this->bits.find(elem) == this->bits.end()) {
                this->bits.insert(elem);
            } else {
                this->bits.erase(elem);
            }
        }
    }

    // Compute this / other and return the remainder
    Bitstream div(const Bitstream &divisor) {
        Bitstream remainder(*this);
        // Compute max terms of remainder and divisor:
        int remainder_max = *std::max_element(remainder.bits.begin(),
                                              remainder.bits.end());
        int divisor_max = *std::max_element(divisor.bits.begin(), divisor.bits.end());
        // While remainder has a larger term than the divisor:
        while (remainder_max >= divisor_max) {
            // Compute next term of quotient and update remainder:
            auto temp = divisor.single_mult(remainder_max - divisor_max);
            remainder.add(temp);
            remainder_max = *std::max_element(remainder.bits.begin(),
                                              remainder.bits.end());
        }
        return std::move(remainder);
    }

    // Return this multiplied by single term "term" without changing this
    Bitstream single_mult(int term) const {
        Bitstream res;
        for (int elem : this->bits) {
            res.bits.insert(elem + term);
        }
        return std::move(res);
    }

    std::string to_string() const {
        std::string str;
        int max = *std::max_element(this->bits.begin(), this->bits.end());
        for (int i = 0; i < max + 1; ++i) {
            str += '0';
        }
        for (auto it = this->bits.begin(); it != this->bits.end(); ++it) {
            str[*it] = '1';
        }
        return std::move(str);
    }

private:
    std::unordered_set<int> bits;
};

bool valid_bit_string(const std::string &str);

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
            Bitstream b1("0000101001");
            std::cout << b1.to_string() << std::endl;
            Bitstream b2("11001");
            std::cout << b2.to_string() << std::endl;
            std::cout << b1.div(b2).to_string() << std::endl;
            ++i; // skip the argument to -c
        } else if (flag == "-v") {

        } else if (flag == "-f") {

        } else if (flag == "-t") {

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
