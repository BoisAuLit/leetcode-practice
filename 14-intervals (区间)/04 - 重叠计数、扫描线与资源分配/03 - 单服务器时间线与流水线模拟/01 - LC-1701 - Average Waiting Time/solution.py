"""LC-1701 - Average Waiting Time

Level 1 · 04 重叠计数、扫描线与资源分配 → Level 2 · 03 单服务器时间线与流水线模拟

题目在问：一个厨师**按给定顺序**做菜，`customers[i] = [arrival, duration]`。
顾客的等待时间 = 他的菜做完的时刻 − 他到达的时刻。求平均等待时间。

### 整道题只有一行递推

```python
free_at = max(free_at, arrival) + duration    # ! 厨师下一次空闲的时刻
wait   += free_at - arrival                   # ! 这位顾客等了多久
```

`max(free_at, arrival)` 的两种情形，就是这题的全部分支：

| 情形 | 含义 | 开始做菜的时刻 |
|---|---|---|
| `free_at <= arrival` | 厨师闲着等人 | `arrival`（顾客一到就开火） |
| `free_at > arrival` | 顾客排队等厨师 | `free_at`（前一单做完才轮到） |

原有代码（`Solution`）把这两种情形写成了显式的 `if / else`，
`Solution_2` 用一个 `max` 把它们合并 —— **同一个递推的两种写法**，没有优劣之分，
但合并版少一处可错的分支（原文件里被注释掉的那段就是它）。

### 为什么这题放在「区间」专题，而且**不是**贪心题

把每单的加工过程看成时间轴上的一段占用区间 `[开始, 结束]`：

```
顾客:    arrival₀      arrival₁   arrival₂
         |             |          |
占用:    [====d₀====][=====d₁=====][==d₂==]      ← 首尾相接，永不重叠
         ↑
         厨师只有一个 ⟹ 任意时刻至多一段
```

⟹ **这是 LC-0253 Meeting Rooms II 的「只有 1 个会议室」特例**：
资源数固定为 1，所以不存在「选哪个」的自由度，
**顺序是题目钦定的（FIFO），没有任何贪心决策** —— 它是整个 Level 1 的基线：
先看清「资源数 = 1、顺序固定」时时间线长什么样，
再去看 LC-0253（多资源）和 LC-1094 Car Pooling（带容量）怎么加维度。

> 顺手一个反直觉事实：按 `duration` 升序重排顾客（SJF 最短作业优先）能让**平均等待时间更小**，
> 这是排队论里的经典结论。但本题**禁止重排** —— 看清这一点，就不会白费力气去想贪心。

### 两个坑

- **整数溢出（C++ / Java）**：`1 <= customers.length <= 10^5`，`arrival <= 10^8`，
  `duration <= 10^3`。最坏情况下 `free_at` 能到 `10^8 + 10^5·10^3 ≈ 2·10^8`，
  而等待时间的**总和**可达 `10^5 · 2·10^8 = 2·10^13` ⟹ **爆 int32**，必须 `long long`。
  Python 整数任意精度，不受影响。
- **浮点精度**：全程用**整数**累加总等待时间，**最后只除一次**。
  如果每一项都 `total += (…) / n`，会累积 10^5 次舍入误差。

### 四种实现

| | 解法 | 时间 | 空间 |
|---|---|---|---|
| `Solution` | 显式 `if / else` 分支（原有代码） | O(n) | O(1) |
| `Solution_2` ⭐️ | `max` 合并分支 | O(n) | O(1) |
| `Solution_3` | 显式造出占用区间（区间视角） | O(n) | O(n) |
| `Solution_4` | 逐秒推进的定义式模拟（真值基线） | O(Σduration) | O(1) |
"""


##################################################################################################
##### ! Solution 1: 显式 if / else 分支（= 下面的 class Solution，用户原有代码，未改动）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：把「厨师等人」和「顾客排队」两种情形分开写，最贴近口述推导的样子。
#####         注意它单独处理了 customers[0]（第一单一定不排队），所以循环从 1 开始
##### ! 本文件下方被注释掉的那段，就是 Solution_2 的 max 合并版（用户原有注释，保留）
##################################################################################################


from typing import List

"""
Time complexity: O()
Space complexity: O()
"""

class Solution:
    def averageWaitingTime(self, customers: List[List[int]]) -> float:
        total_waiting_time = customers[0][1]
        last_order_end_time = customers[0][0] + customers[0][1]
        for arrival_time, duration in customers[1:]:
            if last_order_end_time < arrival_time:
                total_waiting_time += duration
                last_order_end_time = arrival_time + duration
            else:
                total_waiting_time += last_order_end_time - arrival_time + duration
                last_order_end_time = last_order_end_time + duration
        return total_waiting_time / len(customers)


# class Solution:
#     def averageWaitingTime(self, customers: List[List[int]]) -> float:
#         next_idle_time = 0
#         net_wait_time = 0

#         for customer in customers:
#             # The next idle time for the chef is given by the time of delivery
#             # of current customer's order.
#             next_idle_time = max(customer[0], next_idle_time) + customer[1]

#             # The wait time for the current customer is the difference between
#             # his delivery time and arrival time.
#             net_wait_time += next_idle_time - customer[0]

#         # Divide by total customers to get average.
#         average_wait_time = net_wait_time / len(customers)
#         return average_wait_time


s = Solution()
input_ = [[1, 2], [2, 5], [4, 3]]
result = s.averageWaitingTime(input_)
print(result)


##################################################################################################
##### ! Solution 2: 一个 max 合并两种情形（整道题压缩成两行）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：面试首选。free_at = max(free_at, arrival) + duration 同时覆盖
#####         「厨师闲着等人」和「顾客排队等厨师」，少一处可错的分支；
#####         free_at 初值 0 也顺带罩住了第一单，不必特判
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_2:
    def averageWaitingTime(self, customers: List[List[int]]) -> float:
        free_at = 0                         # ! 厨师下一次空闲的时刻
        total = 0                           # ! 用整数累加，最后只除一次（避免 n 次舍入）
        for arrival, duration in customers:
            free_at = max(free_at, arrival) + duration
            total += free_at - arrival      # ! 等待 = 出菜时刻 − 到达时刻
        return total / len(customers)


##################################################################################################
##### ! Solution 3: 显式造出占用区间（本专题的区间视角）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)（存下区间；只求答案时不需要）
##### ! 适用：想把这题和 LC-0253 / LC-1094 放在同一张图里看时。
#####         它把递推的中间状态物化成 [start, end] 列表 ——
#####         断言「这些区间首尾相接、永不重叠」正是「只有一个厨师」的形式化表述
##################################################################################################


class Solution_3:
    def averageWaitingTime(self, customers: List[List[int]]) -> float:
        spans = []                          # ! spans[i] = 第 i 单的加工区间 [start, end]
        prev_end = 0
        for arrival, duration in customers:
            start = max(prev_end, arrival)  # ! 不能早于顾客到达，也不能早于前一单结束
            end = start + duration
            spans.append((start, end))
            prev_end = end
        # ! 不变量：区间两两不重叠（单资源），且按时间递增
        for (s1, e1), (s2, e2) in zip(spans, spans[1:]):
            assert e1 <= s2, "单个厨师不可能同时做两单"
        total = sum(end - arrival for (arrival, _), (_, end) in zip(customers, spans))
        return total / len(customers)


##################################################################################################
##### ! Solution 4: 逐秒推进的定义式模拟（真值基线，只用于测试）
##### ! 时间复杂度: O(Σduration)   空间复杂度: O(1)
##### ! 适用：**不用任何递推公式**，一秒一秒地走时钟：厨师空了就等顾客，
#####         顾客到了就一秒一秒地做菜。它是下面随机对拍的真值来源
##################################################################################################


class Solution_4:
    def averageWaitingTime(self, customers: List[List[int]]) -> float:
        clock = 0
        total = 0
        for arrival, duration in customers:
            while clock < arrival:          # ! 厨师闲着，一秒一秒地等
                clock += 1
            for _ in range(duration):       # ! 一秒一秒地做菜
                clock += 1
            total += clock - arrival
        return total / len(customers)


if __name__ == "__main__":
    import random
    from fractions import Fraction

    IMPLS = [Solution, Solution_2, Solution_3]

    # ! 官方样例
    CASES = [
        ([[1, 2], [2, 5], [4, 3]], 5.0),                    # ! 官方样例 1
        ([[5, 2], [5, 4], [10, 3], [20, 1]], 3.25),         # ! 官方样例 2
        ([[1, 1]], 1.0),                                    # ! 边界：只有一个顾客
        ([[0, 1], [0, 1], [0, 1]], 2.0),                    # ! 全在 0 时刻到达 ⟹ 排成一列
        ([[1, 1], [10, 1], [20, 1]], 1.0),                  # ! 从不排队，等待就是 duration
        ([[3, 10], [4, 1], [5, 1]], (10 + 10 + 10) / 3),    # ! 第一单很长，后面全在排队
    ]
    for customers, want in CASES:
        got_base = Solution_4().averageWaitingTime([c[:] for c in customers])
        assert abs(got_base - want) < 1e-9, ("真值基线自己错了", customers, got_base, want)
        for cls in IMPLS:
            got = cls().averageWaitingTime([c[:] for c in customers])
            assert abs(got - want) < 1e-9, (cls.__name__, customers, got, want)

    # ! 随机对拍：三种 O(n) 实现 vs 逐秒模拟 vs 精确有理数
    random.seed(1701)
    for _ in range(4000):
        n = random.randint(1, 8)
        customers = sorted(
            [[random.randint(0, 15), random.randint(1, 6)] for _ in range(n)],
            key=lambda c: c[0],             # ! 题目保证 arrival 非递减
        )
        want = Solution_4().averageWaitingTime([c[:] for c in customers])
        for cls in IMPLS:
            got = cls().averageWaitingTime([c[:] for c in customers])
            assert abs(got - want) < 1e-9, (cls.__name__, customers, got, want)
        # ! 再用 Fraction 精确算一遍，确认浮点除法没有偏差
        free_at = 0
        total = 0
        for arrival, duration in customers:
            free_at = max(free_at, arrival) + duration
            total += free_at - arrival
        assert abs(float(Fraction(total, n)) - want) < 1e-12

    # ! 溢出守卫（Python 不会溢出，但要能算 ⟹ 顺手确认量级）
    big = [[10 ** 8, 1000]] * 1000
    total_big = Solution_2().averageWaitingTime(big)
    assert total_big > 500_000, total_big     # ! 平均等待约 50 万秒，C++ 里总和会爆 int32

    print("三种 O(n) 实现 + 逐秒真值基线 + Fraction 精确值：6 组定点 + 4000 组随机对拍全部一致 ✓")
    print("averageWaitingTime([[1,2],[2,5],[4,3]])          =",
          Solution_2().averageWaitingTime([[1, 2], [2, 5], [4, 3]]))
    print("averageWaitingTime([[5,2],[5,4],[10,3],[20,1]])  =",
          Solution_2().averageWaitingTime([[5, 2], [5, 4], [10, 3], [20, 1]]))
