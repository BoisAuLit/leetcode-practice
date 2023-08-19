class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        while n:
            count += 1
            n &= n - 1
        return count


# Solution 2 --> Loop
class Solution:
    def hammingWeight(self, n: int) -> int:
        count = 0
        for i in range(32):
            count += n & 1
            n = n >> 1
        return count
