# Largest Rectangle In Histogram 笔记

### 📝 2026-10-17 - retry 1

```python
class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        heights = [0] + heights + [0]      # 左右各加一堵高度 0 的墙
        stack = [0]                        # 栈底放左墙(下标 0),它永远不会被弹出
        res = 0
        for i in range(1, len(heights)):
            while heights[i] < heights[stack[-1]]:
                top = stack.pop()
                left = stack[-1]           # 栈永远不空,不需要 else -1
                res = max(res, (i - left - 1) * heights[top])
            stack.append(i)
        return res
```
