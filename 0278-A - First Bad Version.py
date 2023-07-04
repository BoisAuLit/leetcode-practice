"""
Time complexity: O(logn)
Space complexity: O(1)
"""


def isBadVersion(n: int) -> bool:
    return n >= 2


class Solution:
    def firstBadVersion(self, n: int) -> int:
        left = 1
        right = n

        while left <= right:
            mid = (left + right) // 2
            if isBadVersion(mid):
                if mid - 1 < 1:
                    return 1
                if not isBadVersion(mid - 1):
                    return mid
                right = mid
            else:
                left = mid + 1


s = Solution()
input_ = 2
result = s.firstBadVersion(input_)
print(result)

"""
Runtime
- 45 ms
- Beats 61.78%

Memory
- 16.2 MB
- Beats 96.19%
"""
