class Solution:
    def integerBreak(self, n: int) -> int:

        if n == 2:
            return 1
        if n == 3:
            return 2

        quotient, remainder = divmod(n, 3)
        return 3**quotient * (2 + 2**remainder) // 3


s = Solution()


# Expecting, 1, 2, 4, 36, 54
nums = [2, 3, 4, 10, 11]

for num in nums:
    print(s.integerBreak(num))
