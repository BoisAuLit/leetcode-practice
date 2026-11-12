from typing import List


class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        res = []
        nums.sort()

        def dfs(i, cur, total):
            if total == target:
                res.append(cur.copy())
                return

            for j in range(i, len(nums)):
                if total + nums[j] > target:
                    return
                cur.append(nums[j])
                dfs(j, cur, total + nums[j])
                cur.pop()

        dfs(0, [], 0)
        return res


s = Solution()
input_ = [2, 5, 6, 9]
target = 9                                  # ! 补上漏掉的 target 参数：原来写的是
result = s.combinationSum(input_, target)   # ! s.combinationSum(input_)，少传一个参数，
print(result)                               # ! 整个文件 TypeError 跑不起来
