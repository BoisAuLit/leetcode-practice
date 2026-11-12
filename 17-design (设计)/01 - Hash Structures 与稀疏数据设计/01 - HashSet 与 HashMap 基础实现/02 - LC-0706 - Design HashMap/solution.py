# https://leetcode.com/problems/design-hashmap/

"""
Time complexity: O()
Space complexity: O()
"""

class MyHashMap:

    ARRAY_SIZE = 1000

    def __init__(self):
        self.array = [None] * MyHashMap.ARRAY_SIZE

    def put(self, key: int, value: int) -> None:
        # ! 总是先检查 bucket 是否存在
        if not self.bucket_exists(key):
            self.create_bucket(key)
        # ! 检查完 bucket 的存在之后总是要获取 bucket 的
        bucket = self.get_bucket(key)
        # ! 获取完 bucket 之后总是要遍历 entries 的
        for entry in bucket:
            if entry[0] == key:
                entry[1] = value
                break  # ! key 在 bucket 里唯一，改完就不用再扫剩下的
        else:
            # ! for ... else：循环没被 break 打断才进这里 = 整个 bucket 都没这个 key
            bucket.append([key, value])
        

    def get(self, key: int) -> int:
        # ! 总是先检查 bucket 是否存在
        if not self.bucket_exists(key):
            return -1
        # ! 检查完 bucket 的存在之后总是要获取 bucket 的
        bucket = self.get_bucket(key)
        # ! 获取完 bucket 之后总是要遍历 entries 的
        for entry in bucket:
            if entry[0] == key:
                return entry[1]
        return -1
        

    def remove(self, key: int) -> None:
        # ! 总是先检查 bucket 是否存在
        if not self.bucket_exists(key):
            return
        # ! 检查完 bucket 的存在之后总是要获取 bucket 的
        bucket = self.get_bucket(key)
        # ! 获取完 bucket 之后总是要遍历 entries 的
        for index, entry in enumerate(bucket):
            if entry[0] == key:
                # ! 边遍历边删本来是危险的，但紧跟着 break，循环不会再往下走
                del bucket[index]
                break
    
    def get_hash(self, key: int) -> int:
        return key % MyHashMap.ARRAY_SIZE

    def get_bucket(self, key: int) -> list:
        return self.array[self.get_hash(key)]
    
    def create_bucket(self, key: int) -> None:
        self.array[self.get_hash(key)] = []
    
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
