class Solution_1:
    def hammingWeight(self, n: int) -> int:
        count = 0
        while n:
            if n % 2 == 1:
                count += 1
            n >>= 1
        return count

class Solution_2:
    def hammingWeight(self, n: int) -> int:
        res = 0
        while n:
            n &= n - 1
            res += 1
        return res
