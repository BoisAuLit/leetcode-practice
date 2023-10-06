from typing import List

"""
Time complexity: O(N²)
Space complexity: O(1)

根据木桶原理:  两根柱子所围成的面积取决于较低的柱子
初始设定两个指针指向最左边和最右边的两个柱子
每个循环都向更优解答靠近
"""


class Solution:
    def maxArea(self, height: List[int]) -> int:
        maxarea = 0
        left = 0
        right = len(height) - 1
        
        while left < right:
            width = right - left
            maxarea = max(maxarea, min(height[left], height[right]) * width)
            if height[left] <= height[right]:
                left += 1
            else:
                right -= 1
                
        return maxarea




s = Solution()

# Expecting 49
# input_ = [1, 8, 6, 2, 5, 4, 8, 3, 7]

# # Expecting 1
# input_ = [1, 1]

# # Expecting 2
# input_ = [1, 2, 1]

# Expecting 36
input_ = [2,3,10,5,7,8,9]


result = s.maxArea(input_)

print(result)

"""

"""
