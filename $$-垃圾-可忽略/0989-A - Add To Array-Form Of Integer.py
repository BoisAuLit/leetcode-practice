from typing import List

"""
Time complexity: O(max(N,logK))
Space complexity: O(max(N,logK))
"""


class Solution:
    def addToArrayForm(self, num: List[int], k: int) -> List[int]:
        carry = 0
        for i in range(len(num) - 1, -1, -1):
            k, r = divmod(k, 10)
            carry, num[i] = divmod(num[i] + carry + r, 10)
        extra = []
        while k != 0:
            k, r = divmod(k, 10)
            carry, r = divmod(r + carry, 10)
            extra.append(r)
        return [1] + extra[::-1] + num if carry == 1 else extra[::-1] + num


s = Solution()

# Expecting [1, 0, 2, 1]
# num = [2, 1, 5]
# k = 806

# Expecting [3]
# num = [0]
# k = 3

# Expecting [2, 0, 2, 3, 7]
# num = [3, 8, 5]
# k = 19852

# Expecting [1, 0, 0, 0]
num = [9, 9, 9]
k = 1


result = s.addToArrayForm(num, k)
print(result)

"""
Runtime
- 289ms
- Beats 60.81%

Memory
- 17.50mb
- Beats 31.92%
"""
