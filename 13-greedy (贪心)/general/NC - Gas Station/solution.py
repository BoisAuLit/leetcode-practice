from typing import List


class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        total = 0   # 全程净油量，判断是否有解
        tank = 0    # 从当前候选起点出发的油量
        start = 0   # 当前候选起点

        for i in range(len(gas)):
            diff = gas[i] - cost[i]
            total += diff
            tank += diff
            if tank < 0:          # 从 start 出发撑不过第 i 站
                start = i + 1     # 候选起点直接跳到 i+1
                tank = 0          # 重新计油

        return start if total >= 0 else -1


s = Solution()
gas = [5, 8, 2, 8]
cost = [6, 5, 6, 6]
result = s.canCompleteCircuit(gas, cost)
print(result)
