from typing import List

"""
Time complexity: O(N²)
Space complexity: O(N)
"""

class Solution:
    def rotateString(self, s: str, goal: str) -> bool:
        return len(s) == len(goal) and goal in s * 2

