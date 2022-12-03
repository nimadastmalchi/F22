

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
    def __iter__(self):
        return HashTableIterator(self)

class HashTableIterator:
    def __init__(self, hashTable : HashTable):
        self.hashTable = hashTable
        self.generator = hashTableGenerator(self.hashTable)

    def __next__(self):
        return next(self.generator)

def hashTableGenerator(hashTable : HashTable):
    for current in hashTable.array:
        while current != None:
            yield current.value
            current = current.next

ht = HashTable(10)
ht.insert(10)
ht.insert(20)
ht.insert(30)
for x in ht:
    print(x)

# Output:
# 30
# 20
# 10
