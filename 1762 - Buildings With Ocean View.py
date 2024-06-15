from typing import List

"""
Time complexity: O()
Space complexity: O()
"""

class Solution:
    def findBuildings(self, heights: List[int]) -> List[int]:
        result = []
        max_height = heights[-1]-1
        for i in range(len(heights) - 1, -1, -1):
            if heights[i] > max_height:
                result.append(i)
                max_height = heights[i]
        return result[::-1]


s = Solution()
input_ = [4, 2, 3, 1]
result = s.findBuildings(input_)
print(result)
