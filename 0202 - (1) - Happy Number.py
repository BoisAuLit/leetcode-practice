"""
Time complexity: O(logn)
Space complexity: O(lognb)
"""


class Solution2:
    def get_square_sum(self, n: int) -> int:
        sum_ = 0
        while n != 0:
            n, remainder = divmod(n, 10)
            sum_ += remainder * remainder
        return sum_

    def isHappy(self, n: int) -> bool:
        s = set()
        while True:
            next_ = self.get_square_sum(n)
            if next_ == 1:
                return True
            if next_ in s:
                return False
            n = next_
            s.add(next_)  # 这里忘记过一次


s = Solution2()
input_ = 19  # Expecting True
# input_ = 2 # Expecting False
result = s.isHappy(input_)
print(result)

"""
Runtime
- 45 ms
- Beats 84.12%

Memory
- 16.4 MB
- Beats 31.64%
"""
