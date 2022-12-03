

class Node:
    def __init__(self, val):
        self.value = val
        self.next = None

class HashTable:
    def __init__(self, buckets):
        self.array = [None] * buckets
    def insert(self, val):
        bucket = hash(val) % len(self.array)
        tmp_head = Node(val)
        tmp_head.next = self.array[bucket]
        self.array[bucket] = tmp_head
    def forEach(self, f):
        for current in self.array:
            while current is not None:
                f(current.value)
                current = current.next

    def __iter__(self):
        return HashTableIterator(self.array)

class HashTableIterator:
    def __init__(self, array):
        self.flat_array = []
        # create a flat array that contains all elements of the hash table so
        # we can iterate through all elements of the hash table with 1 pos index
        for current in array:
            while current is not None:
                self.flat_array.append(current)
                current = current.next
        # save the current position in the flat_array
        self.pos = 0
    def __next__(self):
        if self.pos >= len(self.flat_array):
            raise StopIteration()
        ret = self.flat_array[self.pos]
        self.pos += 1
        return ret.value

ht = HashTable(10)
ht.insert(10)
ht.insert(20)
ht.insert(30)

ht.forEach(lambda x: print(x))

# Output:
# 30
# 20
# 10