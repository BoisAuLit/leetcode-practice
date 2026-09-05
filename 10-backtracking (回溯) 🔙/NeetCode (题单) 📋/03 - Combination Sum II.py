from typing import List


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        res = []
        candidates.sort()

        # 进入 backtrack 时恒有 total <= target(由下面的 break 保证)
        def backtrack(i, curr, total):
            if total == target:
                res.append(curr[:])
                return
            for j in range(i, len(candidates)):
                # 同一层里,一个值只让它的第一次出现开分支:
                # j > i 说明本层前面已有兄弟用过这个值,那条分支的结果是它的子集
                if j > i and candidates[j] == candidates[j - 1]:
                    continue
                # 已排序,后面只会更大,直接结束本层
                if total + candidates[j] > target:
                    break
                curr.append(candidates[j])
                backtrack(j + 1, curr, total + candidates[j])
                curr.pop()

        backtrack(0, [], 0)
        return res


s = Solution()
candidates = [9, 2, 2, 4, 6, 1, 5]
target = 8
result = s.combinationSum2(candidates, target)
print(result)
