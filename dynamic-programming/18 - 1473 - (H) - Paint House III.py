from typing import List


class Solution:
    def minCost(
        self,
        houses: List[int],
        cost: List[List[int]],
        m: int,
        n: int,
        target: int,
    ) -> int:
        # ! Check if nb of existing neighborhoods > target
        nei = set()
        for color in houses:
            if color != 0:
                nei.add(color)
        if target < len(nei):
            return -1
