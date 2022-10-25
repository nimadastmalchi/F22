#include <string>
#include <set>

// Represents a bitstream
class Bitstream {
    friend Bitstream get_remainder(const Bitstream &dividend, const Bitstream &divisor);
    friend Bitstream add(const Bitstream &a, const Bitstream &b);
public:
    Bitstream(std::string bitstream="");
    Bitstream(int bits[], int size);
    void add(const Bitstream &other);
    Bitstream single_mult(int term) const;
    std::string to_string() const;
    bool is_zero() const;
    int num_bits() const;
private:
    std::set<int> bits;
};

// Bitstream operations:
Bitstream get_remainder(const Bitstream &dividend, const Bitstream &divisor);
Bitstream add(const Bitstream &a, const Bitstream &b);