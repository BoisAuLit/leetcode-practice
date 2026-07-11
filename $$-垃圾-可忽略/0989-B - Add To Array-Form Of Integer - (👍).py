from typing import List

"""
Time complexity: O(max(N,logK))
Space complexity: O(max(N,logK))
"""


class Solution:
    def addToArrayForm(self, A: List[int], K: int) -> List[int]:
        A[-1] += K
        for i in range(len(A) - 1, -1, -1):
            carry, A[i] = divmod(A[i], 10)
            if i:
                A[i - 1] += carry
        if carry:
            A = list(map(int, str(carry))) + A
        return A


s = Solution()

# Expecting [1, 0, 2, 1]
# num = [2, 1, 5]
# k = 806

# Expecting [3]
# num = [0]
# k = 3

# Expecting [2, 0, 2, 3, 7]
num = [3, 8, 5]
k = 19852

# Expecting [1, 0, 0, 0]
# num = [9, 9, 9]
# k = 1


result = s.addToArrayForm(num, k)
print(result)

"""
Runtime
- 277ms
- Beats 74.74%

Memory
- 17.36mb
- Beats 88.15%
"""
