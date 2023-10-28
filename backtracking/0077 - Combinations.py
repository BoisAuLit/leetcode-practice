from typing import List

"""
Time complexity: O( n! / ((k-1)! ﹒ (n-k)! ))
Space complexity: O(k)
"""


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        def backtrack(
            start: int,
            currentCombination: List[int],
            allCombinations: List[List[int]],
        ):
            if len(currentCombination) == k:
                allCombinations.append(currentCombination.copy())
                return
            for i in range(start, n + 1):
                currentCombination.append(i)
                backtrack(i + 1, currentCombination, allCombinations)
                currentCombination.pop()

        allCombinations = []
        backtrack(1, [], allCombinations)
        return allCombinations


s = Solution()
n = 4
k = 2
result = s.combine(n, k)
print(result)
