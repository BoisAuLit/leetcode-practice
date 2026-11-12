# Degree of an Array 笔记

### 📝 2026-11-02 - retry 1

```python
class Solution:
    def findShortestSubArray(self, nums: List[int]) -> int:
        counter = {}
        res = len(nums)
        max_freq = 0
        print(f"nums = {nums}")
        for i, v in enumerate(nums):
            if v not in counter:
                counter[v] = [1, i, i]  # [freq, index_start, index_end]
            else:
                counter[v][0] += 1
                counter[v][2] = i
            if counter[v][0] > max_freq:
                max_freq = counter[v][0]
                res = counter[v][2] - counter[v][1] + 1
            elif counter[v][0] == max_freq:
                res = min(res, counter[v][2] - counter[v][1] + 1)
        return res
```
