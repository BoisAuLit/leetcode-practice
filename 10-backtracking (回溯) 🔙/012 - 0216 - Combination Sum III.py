from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        candidates = list(range(1, 10))
        length = len(candidates)

        def backtrack(
            start: int,
            remain: int,
            combination: List[int],
            allCombinations: List[List[int]],
        ) -> bool:
            if remain == 0 and len(combination) == k:
                allCombinations.append(combination.copy())
                return True
            if remain < 0:
                return True
            for i in range(start, length):
                combination.append(candidates[i])
                terminate = backtrack(
                    i + 1, remain - candidates[i], combination, allCombinations
                )
                combination.pop()
                if terminate:
                    break

        allCombinations = []
        backtrack(0, n, [], allCombinations)
        return allCombinations


s = Solution()

k = 3
n = 7

result = s.combinationSum3(k, n)

print(result)
