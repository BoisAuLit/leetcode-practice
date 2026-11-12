from typing import List

from collections import defaultdict

class CountSquares:

    def __init__(self):
        self.cnt = defaultdict(int)          # (x, y) -> 该坐标上的点数

    def add(self, point: List[int]) -> None:
        self.cnt[(point[0], point[1])] += 1

    def count(self, point: List[int]) -> int:
        x, y = point
        total = 0
        for (x1, y1), a in list(self.cnt.items()):   # 枚举谁当对角
            if abs(x1 - x) != abs(y1 - y) or x1 == x:  # 必须等距,且不能重合
                continue
            total += a * self.cnt[(x, y1)] * self.cnt[(x1, y)]   # 乘法原理
        return total
