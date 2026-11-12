"""LC-1552 - Magnetic Force Between Two Balls

Level 1 · 03 二分答案与可行性判断 —— **Maximize the Minimum**（最大化最小值）
题目在问：在 position 给出的篮子里放 m 个球，使**任意两球间的最小距离**尽量大，求这个最大值。

这是 Level 2 `02` 的**镜像**，务必和 Minimize Maximum 对照着记：

|  | Minimize Maximum（LC-0410 / 1011） | Maximize Minimum（本题） |
|---|---|---|
| 要找的 | **最小**的可行 limit | **最大**的可行 distance |
| feasible 随参数 | 变大 → 更容易可行 | 变大 → **更难**可行 |
| 谓词形状 | `F F F T T T` | `T T T F F F` |
| 二分目标 | **First True** | **Last True** |
| 边界更新 | 可行 → `hi = mid` | 可行 → `lo = mid` |

**Last True 的死循环陷阱**（本题最容易踩的坑）：
      写 `lo = mid` 时，如果 `mid = (lo + hi) // 2`（向下取整），
      当 `hi == lo + 1` 时 mid 恒等于 lo，`lo = mid` 什么都没变 ⟹ **死循环**。
      解决：Last True 必须用**向上取整的 mid**：`mid = (lo + hi + 1) // 2`。
      记法：「更新哪边，mid 就往哪边偏」。

二分答案三件套：
  1. **先排序**（题目给的 position 是乱序的）。
  2. **答案空间**：`lo = 1`（至少隔 1），`hi = (max - min) // (m - 1)`
     （m 个球最多均匀摊开；用 `max - min` 也可以，只是多几轮）。
  3. **feasible(d)**：贪心放球 —— 第一个球放最左边，之后只要距离 >= d 就放。
     能放满 m 个就可行。

为什么贪心放置是最优的：
      要放尽量多的球，第一个球放最左一定不亏（放更右只会让后面空间更小）；
      之后「一满足距离就立刻放」也不亏 —— 推迟放只会让后续可用位置更少。
      所以贪心能放的球数就是该 d 下的最大球数。

为什么必须先排序：
      贪心依赖「从左到右扫描位置」这个顺序；位置乱序时「距离 >= d 就放」毫无意义。

复杂度：**O(n log n + n · log(range))** —— 排序 + 二分，空间 O(1)（不算排序）。
      不能因为二分部分是 O(n log range) 就忽略排序那一项。

边界：
  - position=[1,2,3,4,7], m=3 → 3
  - position=[5,4,3,2,1,1000000000], m=2 → 999999999
  - m == 2 → 答案就是 max - min
  - m == n → 答案是相邻间隔的最小值
  - 有重复位置（距离 0）
"""

from typing import List


##################################################################################################
##### ! Solution 1: 排序 + 二分答案（Last True）+ 贪心放球
##### ! 时间复杂度: O(n log n + n · log(range))   空间复杂度: O(1) 额外
##### ! 适用：所有「最大化最小间隔 / 最小收益」的题；注意 mid 必须向上取整
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maxDistance(self, position: List[int], m: int) -> int:
        position = sorted(position)          # ! 必须排序，贪心依赖从左到右的顺序
        n = len(position)

        def feasible(d: int) -> bool:
            count, last = 1, position[0]     # ! 第一个球放最左边一定不亏
            for p in position[1:]:
                if p - last >= d:            # ! 够远就立刻放，推迟只会更亏
                    count += 1
                    last = p
                    if count >= m:
                        return True
            return count >= m

        lo, hi = 1, (position[-1] - position[0]) // (m - 1)
        while lo < hi:
            mid = (lo + hi + 1) // 2         # ! Last True 必须向上取整，否则 lo = mid 会死循环
            if feasible(mid):
                lo = mid                     # ! 可行 → 试更大的距离
            else:
                hi = mid - 1
        return lo


##################################################################################################
##### ! Solution 2: 闭区间 + 显式记录候选答案（不用担心向上取整的坑）
##### ! 时间复杂度: O(n log n + n · log(range))   空间复杂度: O(1) 额外
##### ! 适用：怕写错 Last True 的 mid 偏向时，这版用 ans 变量把问题绕开
##################################################################################################


class Solution_2:
    def maxDistance(self, position: List[int], m: int) -> int:
        position = sorted(position)

        def can_place(d: int) -> int:
            count, last = 1, position[0]
            for p in position[1:]:
                if p - last >= d:
                    count += 1
                    last = p
            return count

        lo, hi, ans = 1, position[-1] - position[0], 1
        while lo <= hi:                      # ! 闭区间，mid 照常向下取整
            mid = (lo + hi) // 2
            if can_place(mid) >= m:
                ans = mid                    # ! 记下候选，继续往大了试
                lo = mid + 1
            else:
                hi = mid - 1
        return ans


##################################################################################################
##### ! Solution 3: 枚举所有可能的距离（基准答案，用来对拍）
##### ! 时间复杂度: O(n · range)   空间复杂度: O(1)
##### ! 适用：正确性参照，同时验证 feasible 确实是 T...TF...F 形状
##################################################################################################


class Solution_3:
    def maxDistance(self, position: List[int], m: int) -> int:
        position = sorted(position)

        def can_place(d: int) -> int:
            count, last = 1, position[0]
            for p in position[1:]:
                if p - last >= d:
                    count += 1
                    last = p
            return count

        best = 0
        for d in range(1, position[-1] - position[0] + 1):
            if can_place(d) >= m:
                best = d
        return best


if __name__ == "__main__":
    import random

    cases = [([1, 2, 3, 4, 7], 3), ([5, 4, 3, 2, 1, 1000000000], 2), ([1, 2, 3, 4, 5], 5),
             ([1, 10], 2), ([79, 74, 57, 22], 4)]
    for pos, m in cases:
        a = Solution_1().maxDistance(pos, m)
        assert a == Solution_2().maxDistance(pos, m), (pos, m, a, Solution_2().maxDistance(pos, m))
        print(f"position={pos}, m={m} -> {a}")

    for _ in range(500):                 # ! 随机对拍（含重复位置）
        n = random.randint(2, 8)
        pos = random.sample(range(1, 40), n)
        m = random.randint(2, n)
        a, b, c = (Solution_1().maxDistance(pos, m), Solution_2().maxDistance(pos, m),
                   Solution_3().maxDistance(pos, m))
        assert a == b == c, (pos, m, a, b, c)
    print("随机对拍 500 组通过 ✓")
