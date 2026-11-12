# Container With Most Water 笔记

### 📝 2026-10-02 - retry 1

```python
class Solution:
    def maxArea(self, heights: List[int]) -> int:
        l, r = 0, len(heights) - 1
        best = 0
        while l < r:
            best = max(best, min(heights[l], heights[r]) * (r - l))
            if heights[l] < heights[r]:   # 矮的那边已经不可能更好,排除它
                l += 1
            else:
                r -= 1
        return best
```
