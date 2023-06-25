"""
Time complexity: O(1)
Space complexity: O(1)
"""


class Solution:
    def countOdds(self, low: int, high: int) -> int:
        if high % 2 == 0 and low % 2 == 0:
            return (high - low) // 2
        return (high - low) // 2 + 1


s = Solution()
print(s.countOdds(2, 12))  # [Even, Even], expecting 5
print(s.countOdds(1, 11))  # [Odd, Odd], expecting 6
print(s.countOdds(2, 11))  # [Even, Odd], expecting 5
print(s.countOdds(1, 12))  # [Odd, Even], expecting 6
