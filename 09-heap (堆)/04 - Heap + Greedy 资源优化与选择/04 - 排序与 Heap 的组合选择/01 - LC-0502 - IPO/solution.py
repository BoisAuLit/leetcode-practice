"""LC-0502 - IPO

Level 1 · 04 Heap + Greedy —— **排序 + 堆**的经典组合（两个维度分别交给两个结构）
题目在问：初始资本 w，最多做 k 个项目。项目 i 需要资本 `capital[i]`、赚 `profits[i]`。
         做完一个项目利润累加进资本。求 k 次之后的最大资本。

决定性观察（为什么需要两个结构）：
  1. 每一轮，**所有「当前资本够得着」的项目都是可选的**，应该选利润最大的那个
     —— 因为做任何项目都只会让资本变大（利润非负），不会让后续选择变少。
     所以**贪心成立**：每轮选当前可做项目里利润最高的。
  2. 问题是「当前可做」这个集合是**动态变长**的：资本越多，解锁的项目越多。
  3. 于是两个维度分开处理：
     - **按 capital 升序排序** ⟹ 用一个指针顺序「解锁」项目，每个项目只解锁一次。
     - **解锁的项目按 profit 进最大堆** ⟹ 每轮 O(log n) 取出利润最高的。

```python
projects = sorted(zip(capital, profits))
i, heap = 0, []
for _ in range(k):
    while i < n and projects[i][0] <= w:      # 解锁所有买得起的
        heapq.heappush(heap, -projects[i][1])
        i += 1
    if not heap: break                        # 一个都做不了，提前结束
    w += -heapq.heappop(heap)                 # 做利润最大的
return w
```

**为什么贪心是对的（交换论证）**：
设最优解在某一轮没选当前可做的最大利润项目 P，而选了 Q（profit(Q) < profit(P)）。
把这一轮换成 P：资本变得**不小于**原来，所以后续所有本来能做的项目仍然能做，
而总利润不减。重复这个替换，就能把最优解变成贪心解。∎

**两个提前退出**：
  - 堆空了（当前资本做不了任何剩余项目）⟹ 后面也永远做不了（资本不会变） ⟹ break。
  - 做满 k 个。

复杂度：**O(n log n + k log n)** —— 排序主导 + k 次堆操作。空间 O(n)。
      **不要只说 O(k log n)**，排序那一项不能省。

和 LC-2542 的关系：两题都是「一个维度排序、另一个维度用堆」。
  - 502：按 capital 排序（**解锁**用），堆里放 profit（**选最大**）。
  - 2542：按 nums2 排序（**枚举最小值**用），堆里放 nums1（**踢最小**）。
  这是本 Level 2 的主旨：**遇到两个相互牵制的维度，先排序固定一个、再用堆优化另一个。**

边界：
  - k 大于项目总数 → 做完所有能做的
  - 一开始就做不了任何项目 → 返回 w
  - capital 全是 0 → 第一轮就全部解锁
  - 只有一个项目
"""

import heapq
from typing import List


##################################################################################################
##### ! Solution 1: 按 capital 排序 + profit 最大堆，每轮解锁后取最大
##### ! 时间复杂度: O(n log n + k log n)   空间复杂度: O(n)
##### ! 适用：所有「随着状态变好、可选集合单调变大」的贪心选择题
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        projects = sorted(zip(capital, profits))     # ! 按所需资本升序
        n = len(projects)
        i = 0
        heap: List[int] = []                         # ! 最大堆（存负数）
        for _ in range(k):
            while i < n and projects[i][0] <= w:     # ! 解锁所有买得起的；每个项目只解锁一次
                heapq.heappush(heap, -projects[i][1])
                i += 1
            if not heap:
                break                                # ! 做不了任何项目，资本不会再变，提前结束
            w += -heapq.heappop(heap)                # ! 做利润最大的
        return w


##################################################################################################
##### ! Solution 2: 暴力 —— 每轮线性扫描找当前可做的最大利润项目（基准答案，用来对拍）
##### ! 时间复杂度: O(k · n)   空间复杂度: O(n)
##### ! 适用：正确性参照；也最直白地表达贪心策略
##################################################################################################


class Solution_2:
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        used = [False] * len(profits)
        for _ in range(k):
            best, best_i = -1, -1
            for i, (c, p) in enumerate(zip(capital, profits)):
                if not used[i] and c <= w and p > best:
                    best, best_i = p, i
            if best_i == -1:
                break
            used[best_i] = True
            w += best
        return w


if __name__ == "__main__":
    import random

    cases = [(2, 0, [1, 2, 3], [0, 1, 1]), (3, 0, [1, 2, 3], [0, 1, 2]),
             (1, 2, [1, 2, 3], [1, 1, 2]), (10, 0, [5], [5]), (1, 0, [0], [0])]
    for k, w, p, c in cases:
        a = Solution_1().findMaximizedCapital(k, w, p, c)
        b = Solution_2().findMaximizedCapital(k, w, p, c)
        assert a == b, (k, w, p, c, a, b)
        print(f"k={k}, w={w}, profits={p}, capital={c} -> {a}")

    for _ in range(1000):
        n = random.randint(1, 8)
        p = [random.randint(0, 9) for _ in range(n)]
        c = [random.randint(0, 9) for _ in range(n)]
        k = random.randint(1, n + 2)
        w = random.randint(0, 5)
        assert (Solution_1().findMaximizedCapital(k, w, p, c)
                == Solution_2().findMaximizedCapital(k, w, p, c)), (k, w, p, c)
    print("随机对拍 1000 组通过 ✓（排序+堆 == 每轮线性找最大）")
