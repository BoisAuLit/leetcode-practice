from typing import List


"""
Monotonic stack
"""
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        
        stack = []
        res = [0] * len(temperatures)
        for i, temp in enumerate(temperatures):
            while stack and temp > temperatures[stack[-1]]:
                last = stack.pop()
                res[last] = i - last
            stack.append(i)
        return res
