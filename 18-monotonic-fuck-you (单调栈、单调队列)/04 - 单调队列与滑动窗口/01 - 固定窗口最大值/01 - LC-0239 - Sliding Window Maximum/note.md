# Sliding Window Maximum 笔记

### 📝 2026-09-27 - retry 1

```python
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        res = []
        q = deque()
        for i, num in enumerate(nums[:k]):
            while q and num >= nums[q[-1]]:
                q.pop()
            q.append(i)
        res.append(nums[q[0]])
        for i in range(k, len(nums)):
            num = nums[i]

            # ! 注意, 这里不是 q[0] == i - k !!!!!!!!
            if q[0] == i - k: 
                q.popleft()
            while q and num >= nums[q[-1]]:
                q.pop()
            q.append(i)
            res.append(nums[q[0]])
        return res
```

### 📝 2026-10-04 - retry 2

```python
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        res = []
        n = len(nums)
        q = deque()
        for i in range(k):
            while q and nums[i] >= nums[q[-1]]:
                q.pop()
            q.append(i)
        res.append(nums[q[0]])
        for i in range(k, n):
            # ! 注意, 这里一定要是等于, 不是 >
            if i - k == q[0]:
                q.popleft()
            while q and nums[i] >= nums[q[-1]]:
                q.pop()
            q.append(i)
            res.append(nums[q[0]])
        return res
```
