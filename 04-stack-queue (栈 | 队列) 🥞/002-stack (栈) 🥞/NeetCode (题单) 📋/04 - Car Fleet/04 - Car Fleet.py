"""
📌 信号→模式: 车队合并数 → 按起点降序，算到达时间，后车更快则并入前车（单调栈）
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from typing import List


class Solution:
    def carFleet(
        self, target: int, position: List[int], speed: List[int]
    ) -> int:
        pair = sorted([(p, s) for p, s in zip(position, speed)], reverse=True)
        stack = []
        for p, s in pair:  # Reverse Sorted Order
            stack.append((target - p) / s)
            if len(stack) >= 2 and stack[-1] <= stack[-2]:
                stack.pop()
        return len(stack)
