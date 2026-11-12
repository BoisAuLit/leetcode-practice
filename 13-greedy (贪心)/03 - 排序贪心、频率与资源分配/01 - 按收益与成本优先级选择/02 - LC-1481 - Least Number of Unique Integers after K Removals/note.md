# Least Number of Unique Integers after K Removals 笔记

### 📝 2026-10-03 - retry 1

```python
class Solution:
    def findLeastNumOfUniqueInts(self, arr: List[int], k: int) -> int:
        freqs = sorted(Counter(arr).values())  # 频率升序
        remaining = len(freqs)  # 当前还剩多少个不同的数
        for f in freqs:
            if k < f:
                break
            k -= f
            remaining -= 1

        return remaining
```
