#include "Bitstream.h"
#include <algorithm>
#include <iostream>

Bitstream::Bitstream(std::string bitstream) : min_size(0) {
    for (int i = 0; i < bitstream.size(); ++i) {
        if (bitstream[i] == '1') {
            this->bits.insert(bitstream.size() - 1 -i);
        }
    }
}

Bitstream::Bitstream(int bits[], int size) : min_size(0) {
    for (int i = 0; i < size; ++i) {
        this->bits.insert(bits[i]);
    }
}

void Bitstream::add(const Bitstream &other) {
    // For all elements elem of other, if there elem is in this, then remove
    // it. Otherwise, add it (i.e., compute xor).
    for (std::set<int>::iterator it = other.bits.begin();
            it != other.bits.end();
            ++it) {
        if (this->bits.find(*it) == this->bits.end()) {
            this->bits.insert(*it);
        } else {
            this->bits.erase(*it);
        }
    }
}

void Bitstream::set_min_size(int min_size) {
    this->min_size = min_size;
}

// Return this multiplied by single term "term" without changing this
Bitstream Bitstream::single_mult(int term) const {
    Bitstream res;
    for (std::set<int>::iterator it = this->bits.begin();
            it != this->bits.end();
            ++it) {
        res.bits.insert(*it + term);
    }
    return std::move(res);
}

std::string Bitstream::to_string() const {
    std::string str;
    int size = std::max(num_bits(), min_size);
    for (int i = 0; i < size; ++i) {
        str += '0';
    }
    for (std::set<int>::iterator it = this->bits.begin();
            it != this->bits.end();
            ++it) {
        str[size - 1 - *it] = '1';
    }
    return std::move(str);
}

bool Bitstream::is_zero() const {
    return bits.empty();
}

int Bitstream::num_bits() const {
    return bits.empty() ? 0 : *bits.rbegin() + 1;
}

Bitstream get_remainder(const Bitstream &dividend, const Bitstream &divisor) {
    Bitstream remainder(dividend);
    std::cout << dividend.to_string() << std::endl;
    // Compute max terms of remainder and divisor:
    int remainder_max = *remainder.bits.rbegin();
    int divisor_max = *divisor.bits.rbegin();
    // While remainder has a larger term than the divisor:
    while (remainder_max >= divisor_max) {
        // Compute next term of quotient and update remainder:
        Bitstream temp = divisor.single_mult(remainder_max - divisor_max);
        remainder.add(temp);
        if (remainder.bits.empty()) {
            return remainder;
        }
        remainder_max = *remainder.bits.rbegin();
    }
    return std::move(remainder);
}

Bitstream add(const Bitstream &a, const Bitstream &b) {
    Bitstream res(a);
    // For all elements elem of b, if there elem is in a, then remove it.
    // Otherwise, add it (i.e., compute xor).
    for (std::set<int>::iterator it = b.bits.begin();
            it != b.bits.end();
            ++it) {
        if (a.bits.find(*it) == a.bits.end()) {
            res.bits.insert(*it);
        } else {
            res.bits.erase(*it);
        }
    }
    return std::move(res);
}
