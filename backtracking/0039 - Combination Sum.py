from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:

        results = []

        def backtrack(remain, comb, start):
            if remain == 0:
                results.append(comb.copy())
                return
            elif remain < 0:
                return

            for i in range(start, len(candidates)):
                comb.append(candidates[i])
                backtrack(remain - candidates[i], comb, i)
                comb.pop()

        backtrack(target, [], 0)

        return results


s = Solution()

# Expecting [[2,2,3],[7]]
candidates = [2, 3, 6, 7]
target = 7

# Expecting [[2,2,2,2],[2,3,3],[3,5]]
# candidates = [2, 3, 5]
# target = 8


result = s.combinationSum(candidates, target)
print(result)
