// Nima Amir Dastmalchi
// 505320372

#include <string>
#include <set>

// Represents a bitstream
class Bitstream {
    friend Bitstream get_remainder(const Bitstream &dividend, const Bitstream &divisor);
    friend Bitstream add(const Bitstream &a, const Bitstream &b);
public:
    /**
     * Construct a new Bitstream from a string of 0's and 1's.
     */
    Bitstream(std::string bitstream="");

    /**
     * Construct a new Bitstream from the give bitmap "bits".
     */
    Bitstream(int bits[], int size);

    /**
     * Add other to the current Bitstream using mod2 arithmetic.
     */
    void add(const Bitstream &other);

    /**
     * Set a minimum size for the Bitstream. This value will only be used
     * by the to_string() method.
     */
    void set_min_size(int);

    /**
     * Multiply the current Bitstream by the polynomial x^term using mod2
     * arithmetic.
     */
    Bitstream single_mult(int term) const;

    /**
     * Return the string representation of this Bitstream. Use the set_min_size
     * function to specify a minimum number of bits to print out.
     */
    std::string to_string() const;

    /**
     * Return true if the Bitstream is 0 (it has no 1 bits), false otherwise
     */
    bool is_zero() const;

    /**
     * Return the number of bits stored in this Bitstream.
     */
    int num_bits() const;
private:
    std::set<int> bits;
    int min_size;
};

// Bitstream operations:
/**
 * Given Bistreams dividend and divisor, return the Bitstream representing the
 * remainder of dividend / divisor using mod2 arithmetic.
 */
Bitstream get_remainder(const Bitstream &dividend, const Bitstream &divisor);

/**
 * Given Bitstreams a and b, return Bitstream a + b using mod 2 arithmetic
 */
Bitstream add(const Bitstream &a, const Bitstream &b);