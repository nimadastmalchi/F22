
class Socket { /* ... */ };
class RoomView {
    RoomView() {
        this.socket = new Socket();
    }

    void dispose() {
        this.socket.cleanupFd();
    }

    ~RoomView() {}
    // ...
};

int main() {
    RoomView *rv = new RoomView();
    // ...
    rv.dispose();
    // Let GC deallocate the object when needed
}

