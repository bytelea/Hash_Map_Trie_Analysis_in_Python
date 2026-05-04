"""HashMap implemented from scratch using an array with separate chaining
for collision resolution but no built-in dict is used for the core structure
Supports:
insert(key, value) O(1) average case
search(key) O(1) average case
__len__ number of inserted entries """

INITIAL_CAPACITY = 262144  # sized for over 175k entries (dataset times 2)

class HashMapEntry:
    """single key value pair stored inside a bucket chain"""
    def __init__(self, key: str, value):
        self.key = key
        self.value = value
        self.next = None # pointer to the next entry in the chain

class HashMap:
    """ hash map using open addressing with separate chaining, each slot in the internal array
    holds a linked-list chain of HashMapEntry objects to handle hash collisions """

    def __init__(self, capacity: int = INITIAL_CAPACITY):
        self.capacity = capacity
        self.buckets = [None] * self.capacity # the underlying array
        self._size = 0

    # hash function
    def _hash(self, key: str) -> int:
        """ convert a string key into a valid bucket index, it uses a polynomial rolling hash
        each character's ASCII value is multiplied by a prime raised to its position, summed,
        then reduced modulo the capacity this distributes keys evenly across buckets dnd minimises collisions
        time complexity O(k) where k = len(key) """
        hash_value = 0
        prime = 31

        for i, char in enumerate(key):
            hash_value += ord(char) * (prime ** i)

        return hash_value % self.capacity

    # core operations
    def insert(self, key: str, value) -> None:
        """ insert a key-value pair into the HashMap, if the key already exists, its value is updated in place
        collisions are handled by chaining new entries are prepended to the front of the bucket's linked list
        evg time complexity is O(1) """
        index = self._hash(key)
        entry = self.buckets[index]

        # walk the chain to check for an existing key
        while entry is not None:
            if entry.key == key:
                entry.value = value # update existing
                return
            entry = entry.next

        # prepend a new entry at the head of the chain
        new_entry = HashMapEntry(key, value)
        new_entry.next = self.buckets[index]
        self.buckets[index] = new_entry
        self._size += 1

    def search(self, key: str):
        """ look up a key and return its associated value, or None if not found
        avg time complexity is O(1)
        worst case is (all keys collide) O(n) """
        index = self._hash(key)
        entry = self.buckets[index]

        while entry is not None:
            if entry.key == key:
                return entry.value
            entry = entry.next

        return None

    # utility
    def __len__(self) -> int:
        return self._size

    def load_factor(self) -> float:
        """ratio of entries to buckets indicates how full the map is"""
        return self._size / self.capacity

    def collision_stats(self) -> dict:
        """ returns stats about chain lengths for analysis"""
        chain_lengths = []
        for bucket in self.buckets:
            length = 0
            entry = bucket
            while entry is not None:
                length += 1
                entry = entry.next
            chain_lengths.append(length)

        non_empty = [l for l in chain_lengths if l > 0]
        return {
            "total_entries": self._size,
            "capacity": self.capacity,
            "load_factor": round(self.load_factor(), 4),
            "non_empty_buckets": len(non_empty),
            "max_chain_length": max(chain_lengths) if chain_lengths else 0,
            "avg_chain_length": round(sum(non_empty) / len(non_empty), 4) if non_empty else 0,
        }