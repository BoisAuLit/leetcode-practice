from typing import List


class MyHashSet:
    ARRAY_SIZE = 1000

    def __init__(self):
        self.array = [None] * MyHashSet.ARRAY_SIZE

    def add(self, key: int) -> None:
        if not self.bucket_exists(key):
            self.create_bucket(key)
        bucket = self.get_bucket(key)
        if key not in bucket:
            bucket.append(key)

    def remove(self, key: int) -> None:
        if not self.bucket_exists(key):
            return
        bucket = self.get_bucket(key)
        if key in bucket:
            bucket.remove(key)

    def contains(self, key: int) -> bool:
        if not self.bucket_exists(key):
            return False
        return key in self.get_bucket(key)

    def get_hash(self, key: int) -> int:
        return key % MyHashSet.ARRAY_SIZE

    def get_bucket(self, key: int) -> List:
        return self.array[self.get_hash(key)]

    def create_bucket(self, key: int) -> None:
        self.array[self.get_hash(key)] = []

    def bucket_exists(self, key: int) -> bool:
        return self.get_bucket(key) is not None


"""
Runtime
- 162ms
- Beats 76.20%

Memory
21.71mb
- Beats 71.57%
"""
