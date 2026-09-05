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
