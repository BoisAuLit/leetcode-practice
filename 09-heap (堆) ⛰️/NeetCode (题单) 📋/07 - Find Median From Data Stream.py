"""
📌 信号→模式: 动态中位数 → 大根堆（小半）+ 小根堆（大半），保持大小平衡
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
import heapq


class MedianFinder:
    def __init__(self):
        self.even = True
        self.minH = []
        self.maxH = []

    def addNum(self, num: int) -> None:
        if not self.minH:
            self.maxH = [-num]
            self.minH = [num]
            self.even = False
            return

        if self.even:
            if num < -self.maxH[0]:
                heapq.heappush(self.minH, -self.maxH[0])
                heapq.heappush(self.maxH, -num)
            elif -self.maxH[0] <= num <= self.maxH[0]:
                heapq.heappush(self.minH, num)
                heapq.heappush(self.maxH, -num)
            else:
                heapq.heappush(self.maxH, -self.minH[0])
                heapq.heappush(self.minH, num)
        else:
            if num <= -self.maxH[0]:
                heapq.heappop(self.maxH)
                heapq.heappush(self.maxH, -num)
            else:
                heapq.heappop(self.minH)
                heapq.heappush(self.minH, num)
        self.even = not self.even

    def findMedian(self) -> float:
        return (self.minH[0] + (-self.maxH[0])) / 2


medianFinder = MedianFinder()
medianFinder.addNum(5)
medianFinder.addNum(3)
print(medianFinder.findMedian())
medianFinder.addNum(7)
print(medianFinder.findMedian())
medianFinder.addNum(2)
print(medianFinder.findMedian())
