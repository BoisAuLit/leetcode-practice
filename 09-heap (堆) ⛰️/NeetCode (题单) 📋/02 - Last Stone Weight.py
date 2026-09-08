"""
📌 信号→模式: 反复取两最大相碰 → 大根堆（取负）模拟
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from typing import List
import heapq


class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        heap = []
        for stone in stones:
            heapq.heappush(heap, -stone)
        while len(heap) >= 2:
            x = -heapq.heappop(heap)
            y = -heapq.heappop(heap)
            diff = abs(x - y)
            if diff > 0:
                heapq.heappush(heap, -diff)
        return -heap[0] if heap else 0
