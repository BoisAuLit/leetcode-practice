from typing import List


class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        total_sum = sum(nums)
        if abs(target) > abs(total_sum):
            return 0
        m = len(nums)
        n = 2 * total_sum + 1
        dp = [[0] * n for _ in range(len(nums))]

        dp[0][total_sum - nums[0]] = 1
        dp[0][total_sum + nums[0]] += 1

        for i in range(m - 1):
            for j in range(n):
                num = dp[i][j]
                if num > 0:
                    dp[i + 1][j + nums[i + 1]] += num
                    dp[i + 1][j - nums[i + 1]] += num

        return dp[-1][total_sum + target]


s = Solution()

# Test case 1: Expecting 5
nums = [1, 1, 1, 1, 1]
target = 3

# Test case 2: Expecting 2
# nums = [1, 1]
# target = 0

# Test case 3: Expecting 256
# nums = [0, 0, 0, 0, 0, 0, 0, 0, 1]
# target = 1


# Test case 4: Expecting 2
# nums = [1, 0]
# target = 1

result = s.findTargetSumWays(nums, target)
print(result)
