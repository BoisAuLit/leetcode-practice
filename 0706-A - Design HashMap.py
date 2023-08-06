from collections import deque
from typing import Deque
"""
Time complexity: O()
Space complexity: O()
"""

class MyHashMap:

    ARRAY_SIZE = 1000

    def __init__(self):
        self.array = [None] * MyHashMap.ARRAY_SIZE

    def put(self, key: int, value: int) -> None:
        if not self.bucket_exists(key):
            self.create_bucket(key)
        bucket = self.get_bucket(key)
        count = 0
        for entry in bucket:
            if entry[0] == key:
                entry[1] = value
                count += 1
        if count == 0:
            bucket.append([key, value])
        

    def get(self, key: int) -> int:
        if not self.bucket_exists(key):
            return -1
        bucket = self.get_bucket(key)
        for entry in bucket:
            if entry[0] == key:
                return entry[1]
        return -1
        

    def remove(self, key: int) -> None:
        if not self.bucket_exists(key):
            return
        bucket = self.array[self.get_hash(key)]
        index = 0
        found_index = -1
        for entry in bucket:
            if entry[0] == key:
                found_index = index
            index += 1
        if found_index != -1:
            bucket.remove(bucket[found_index])
    
    def get_hash(self, key: int) -> int:
        return key % MyHashMap.ARRAY_SIZE

    def get_bucket(self, key: int) -> Deque:
        return self.array[self.get_hash(key)]
    
    def create_bucket(self, key: int) -> None:
        self.array[self.get_hash(key)] = deque()
    
    def bucket_exists(self, key: int) -> bool:
        return self.get_bucket(key) is not None
        



hashmap = MyHashMap()
hashmap.put(1, 1)
hashmap.put(2, 2)
print(hashmap.get(1)) # Expecting 1
print(hashmap.get(2)) # Expecting 2
print(hashmap.get(3)) # Expecting -1
hashmap.put(2, 1)
print(hashmap.get(2)) # Expecting 1
hashmap.remove(2)
print(hashmap.get(2)) # Expecting -1

"""
Runtime
- 218ms
- Beats 72.98%

Memory
20.88mb
- Beats 24.87%
"""
