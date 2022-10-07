#include <iostream>
#include <assert.h>
#include <vector>

// problem 8a
std::size_t longestRun(std::vector<bool> v) {
    std::size_t ans = 0, cur = 0;
    for (const bool elem : v) {
        if (elem) {
            ++cur;
            ans = std::max(ans, cur);
        } else {
            cur = 0;
        }
    }
    return ans;
}


int main() {
    std::vector<bool> v;
    v.push_back(true);
    v.push_back(true);
    v.push_back(false);
    v.push_back(true);
    v.push_back(true);
    v.push_back(true);
    v.push_back(false);
    std::cout << longestRun(v) << std::endl;
    v.clear();
    v.push_back(true);
    v.push_back(false);
    v.push_back(true);
    v.push_back(true);
    std::cout << longestRun(v) << std::endl;
}

