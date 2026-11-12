# Insert Interval 笔记

### 📝 2026-09-26 - retry 1

```python
class Solution:

    """
    bisect_left 确定的边界是 < x, >= x
    bisect_right 确定的边界是 <= x, > x
    """
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:

        left, right = newInterval
        i = bisect_left(intervals, left, key=lambda x: x[1])
        j = bisect_right(intervals, right, key=lambda x: x[0])

        # ! 倘若 i == j, 说明 newInterval 与所有的其他 interals 都无任何交集
        # ! 这一点很重要
        if i == j:
            return intervals[:i] + [newInterval] + intervals[i:]

        nl = min(left, intervals[i][0])
        nr = max(right, intervals[j - 1][1])  # ! 别忘了这里是 j - 1!!

        return intervals[:i] + [[nl, nr]] + intervals[j:]
```

### 📝 2026-10-01 - retry 2

```python
class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        start, end = newInterval
        i1 = bisect_left(intervals, start, key=lambda x: x[1])
        i2 = bisect_right(intervals, end, key=lambda x:x[0])
        if i1==i2:
            return intervals[:i1] + [newInterval] + intervals[i1:]
        # fmt: off
        return intervals[:i1] + [[
            min(start, intervals[i1][0]),
            max(end, intervals[i2-1][1])
        ]] + intervals[i2:]
```
