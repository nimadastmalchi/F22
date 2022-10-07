#include <iostream>
#include <vector>
#include <stack>
using namespace std;

class Tree {
public:
    unsigned value;
    vector<Tree *> children;

    Tree(unsigned value) : value(value) {}

    Tree(unsigned value, vector<Tree *> children) {
        this->value = value;
        this->children = children;
    }
};

unsigned maxTreeValue(Tree *root) {
    if (root == nullptr) {
        return 0;
    }
    unsigned ans = 0;

    stack<Tree *> process;
    process.push(root);
    while (!process.empty()) {
        Tree *cur = process.top();
        process.pop();

        if (cur->value > ans) {
            ans = cur->value;
        }

        for (auto *ptr : cur->children) {
            if (ptr != nullptr) {
                process.push(ptr);
            }
        }
    }
    return ans;
}

int main() {
    Tree root(10);
    Tree left(5);
    Tree right(15);
    root.children.push_back(&left);
    root.children.push_back(&right);
    cout << maxTreeValue(&root) << endl;
}
