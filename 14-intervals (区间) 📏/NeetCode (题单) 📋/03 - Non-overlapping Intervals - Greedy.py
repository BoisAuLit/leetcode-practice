"""
📌 信号→模式: 最少删除使不重叠 → 按结束时间排序，贪心保留最早结束
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from typing import List


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        # Greedy: keep intervals that end earliest
        intervals.sort(key=lambda x: x[1])

        prevEnd = intervals[0][1]
        removed = 0

        for start, end in intervals[1:]:
            if start < prevEnd:
                # Overlap:
                # remove current interval because the previous one
                # ends no later than it
                removed += 1
            else:
                # No overlap: keep it
                prevEnd = end

        return removed
