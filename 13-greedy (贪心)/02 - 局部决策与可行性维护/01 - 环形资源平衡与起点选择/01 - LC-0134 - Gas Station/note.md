# Gas Station 笔记

### 📝 2026-09-28 - retry 1

```python
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        # 每站只关心净变化 diff = gas - cost;题目 = 在环形 diff 上找一个起点,累加永不为负
        # 两个事实:
        #   ① 有解 ⟺ sum(diff) >= 0
        #   ② 从 start 出发在 i 站第一次变负 → start..i 全部不能当起点,候选直接跳到 i+1
        #      (中途 j 出发 = 扔掉 start..j 攒的油,后面路一样,只会更早/同时挂)
        total = 0    # diff 总和,永不清零,只用来判事实①
        tank = 0     # 从当前 start 出发到现在的油箱,失败就清零
        start = 0    # 当前候选起点

        for i in range(len(gas)):
            diff = gas[i] - cost[i]
            total += diff
            tank += diff
            if tank < 0:          # 事实②:start..i 整段排除
                start = i + 1
                tank = 0

        # 最后一段 [start, n-1] 攒的油 >= 前面被跳过部分的亏空(由 total >= 0 保证),
        # 所以绕回去也不会负,不用二次验证
        return start if total >= 0 else -1
```

### 📝 2026-10-02 - retry 2

```python
class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        total = 0
        i = 0
        res = 0
        whole_gas = 0
        whole_cost = 0
        while i < len(gas):
            whole_gas += gas[i]
            whole_cost += cost[i]
            diff = gas[i] - cost[i]
            total += diff
            if total < 0:
                total = 0
                res = i + 1
            i += 1
        return res if whole_gas >= whole_cost else -1
```
