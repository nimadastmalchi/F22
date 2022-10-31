#include <iostream>

int main() {
    for (int i = 0; i < 1000; ++i) {
        for (int j = i+1; j < 1000; ++j) {
            for (int k = j+1; k < 1000; ++k) {
                for (int l = k+1; l < 1000; ++l) {
                    for (int m = l+1; m < 1000; ++m) {
                        std::cout << i << " " << j << " " << k << " " << l << " " << m << std::endl;
                    }
                }
            }
        }
    }
}
