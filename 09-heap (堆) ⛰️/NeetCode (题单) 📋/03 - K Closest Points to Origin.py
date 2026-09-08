"""
📌 信号→模式: 前 k 近的点 → 大小为 k 的大根堆按距离淘汰；或快速选择
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from typing import List
import heapq


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        heap = []
        for x, y in points:
            dist = x * x + y * y
            if len(heap) < k:
                heapq.heappush(heap, (-dist, x, y))
            else:
                if dist < -heap[0][0]:
                    heapq.heappop(heap)
                    heapq.heappush(heap, (-dist, x, y))
        return [(x, y) for _, x, y in heap]


s = Solution()
points = [[0,2],[2,0],[2,2]]
k = 2
result = s.kClosest(points, k)
print(result)
