from typing import List


class Solution_1:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2 == 1:
            return False
        target = total // 2

        sums = {0}
        for num in nums:
            new_sums = sums.copy()
            for curr_sum in sums:
                new_sum = curr_sum + num
                if new_sum == target:
                    return True
                if new_sum < target:
                    new_sums.add(new_sum)
            sums = new_sums

        return target in sums


class Solution_2:
    def canPartition(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2 == 1:
            return False

        target = total // 2
        """
        dp[i] 表示: 我们能否用 nums 里的数凑出 i 这个 sum
        前提: 每个 nums 里的数只能用一次

        dp[0] = True 的原因: 倘若我们什么数都不用, 那么和就是 0
        """
        dp = [False] * (target + 1)
        dp[0] = True

        for num in nums:
            for curr_sum in range(target, num - 1, -1):
                if dp[curr_sum - num]:
                    dp[curr_sum] = True

        return dp[target]

