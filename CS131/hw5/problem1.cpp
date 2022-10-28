#include <iostream>

class my_shared_ptr {
private:
    int *ptr = nullptr;
    int *refCount = nullptr; // a)

public:
    // b) constructor
    my_shared_ptr(int *ptr) {
        this->ptr = ptr;
        this->refCount = new int(0);
    }

    // c) copy constructor
    my_shared_ptr(const my_shared_ptr & other){
        this->ptr = other.ptr;
        this->refCount = other.refCount;
        ++(*this->refCount); // update the reference count
    }

    // d) destructor
    ~my_shared_ptr() {
        --(*this->refCount);
        if (*this->refCount == 0) {
            delete this->ptr;
            delete this->refCount;
        }
    }

    // e) copy assignment
    my_shared_ptr& operator=(const my_shared_ptr & obj) {
        --(*this->refCount);
        if (*this->refCount == 0) {
            delete this->ptr;
            delete this->refCount;
        }

        this->ptr = obj.ptr;
        this->refCount = obj.refCount;
        ++(*this->refCount);
    }
};

int main() {
    auto ptr1 = new int[100];
    auto ptr2 = new int[200];
    my_shared_ptr m(ptr1); // should create a new shared_ptr for ptr1
    my_shared_ptr n(ptr2); // should create a new shared_ptr for ptr2
    n = m; // ptr2 should be deleted, and there should be 2
    shared_ptr pointing to ptr1
}

