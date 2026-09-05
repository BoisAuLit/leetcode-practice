# Solution 1 --> Bit Manipulate
"""
Instead of checking every bit of the number,
we repeatedly flip the least-significant 111-bit
of the number to 000, and add 111 to the sum.
As soon as the number becomes 000, we know that
it does not have any more 111-bits, and we return the sum.
"""
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
