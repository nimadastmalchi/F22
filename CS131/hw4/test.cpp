#include <iostream>

void boop() {
    if (true) {
        int x = 2;
        beep();
    }
    std::cout << x << std::endl; // x not defined
}

void beep() {
    x = 1; // x not defined
}

int main() {
}