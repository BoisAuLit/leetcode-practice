import math

"""
Time complexity: O(1)
Space complexity: O(1)

Only numbers having odd number of factors will still be on in the end.
Only perfect square numbers have odd number of factors.

Let's look at a non perfect square number 12, its factors are
- 1, 12
- 2, 6
- 3, 4
Then its number of factors must be even.

Let's look at 16
- 1, 16
- 2, 8
- 4
Then its number of factors must be odd because one of the pairs cannot be formed
because these two factors are equal.

"""

class Solution:
    def bulbSwitch(self, n: int) -> int:
        return int(math.sqrt(n))

s = Solution()
n = 3
result = s.bulbSwitch(n)
print(result)
