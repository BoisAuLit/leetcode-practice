from typing import List


class Solution:
    def minCostII(self, costs: List[List[int]]) -> int:
        k = len(costs[0])

        dp = costs[0]
        for i in range(1, len(costs)):
            temp = [0] * k
            for j in range(k):
                temp[j] = costs[i][j] + min(dp[x] for x in range(k) if x != j)
            dp = temp
        return min(dp)

s = Solution()
costs = [[1,5,3],[2,9,4]]
result = s.minCostII(costs)
print(result)
