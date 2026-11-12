# Design HashMap 笔记

### 📝 2026-10-04 - retry 1

```python
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
        count = 0
        # ! 获取完 bucket 之后总是要遍历 entries 的
        for entry in bucket:
            if entry[0] == key:
                entry[1] = value
                count += 1
        if count == 0:
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
        bucket = self.array[self.get_hash(key)]
        index = 0
        found_index = -1
        # ! 获取完 bucket 之后总是要遍历 entries 的
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
```

### 💬 2026-10-13 - finish 🟢

red
