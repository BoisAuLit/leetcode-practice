from collections import defaultdict
from typing import List


"""
Complexity Analysis:
    - Time Complexity: O(n)
    - Space Complexity: O(n)
"""

class Solution:
    def countBlackBlocks(self, m: int, n: int, coordinates: List[List[int]]) -> List[int]:
        block_counts = defaultdict(int)
        for x, y in coordinates:
            for dx, dy in [(-1,-1), (-1,0), (0,-1), (0,0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m - 1 and 0 <= ny < n - 1:
                    block_counts[(nx, ny)] += 1
        arr = [0] * 5
        for count in block_counts.values():
            arr[count] += 1
        total_blocks = (m - 1) * (n - 1)
        arr[0] = total_blocks - sum(arr[1:])
        return arr
