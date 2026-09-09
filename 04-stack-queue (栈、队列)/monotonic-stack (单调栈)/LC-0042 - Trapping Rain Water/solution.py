from typing import List

"""
Time complexity: O(N)
Space complexity: O(N)


"""


class Solution:
    def trap(self, height: List[int]) -> int:
        n = len(height)
        max_r = height[-1]
        for i in range(n - 1, -1, -1):
            max_r = max(max_r, height[i])
            height[i] = (height[i], max_r)
        result = 0
        max_l = height[0][0]
        for i in range(n):
            curr, max_r = height[i]
            max_l = max(max_l, curr)
            if max_l >= curr and max_r >= curr:
                result += min(max_l, max_r) - curr
        return result


s = Solution()
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
result = s.trap(height)
print(result)
