"""LC-2561 - Rearranging Fruits

Level 1 · 03 排序贪心 —— **频率平衡 + 「借最小值」的交换技巧**
题目在问：两个等长篮子，每次可以交换两篮各一个水果，代价是 `min(两者)`。
         要让两篮**完全相同**（多重集相等），求最小总代价；做不到返回 -1。

决定性观察（三步，每步都是关键）：

### ① 可行性与「谁需要被换走」
把两篮合起来统计每种水果的总数 `cnt[v]`。
- **若某个 `cnt[v]` 是奇数 ⟹ 不可能平分 ⟹ 返回 -1。**
- 否则每篮最终各应有 `cnt[v] / 2` 个。
  篮子 1 中**多出来的**那些（超过 `cnt[v]/2` 的部分）组成列表 `extra1`，
  篮子 2 的多余组成 `extra2`。**两个列表长度必然相等。**

### ② 配对：小的配大的
把 `extra1` **升序**、`extra2` **降序**，一一配对
（也就是「1 的最小配 2 的最大」）。每对的代价是 `min(a, b)`。

**为什么这样配最优**：代价只取决于 `min`，所以要让每对的 `min` 尽量小
⟹ 把两边的小元素尽量「配到一起的另一侧是大元素」，
也就是**让小元素承担代价、大元素免费搭车**。
等价地：把 `extra1 + extra2` 合起来排序后，
**代价 = 前一半元素之和**（后一半全部搭车）。这是最简洁的表述。

### ③ 「借最小值」的技巧（本题最精彩的一步）
如果全局最小的水果 `m = min(所有水果)` **不在需要交换的那些元素里**，
我们仍然可以用它来降低代价：
> 要交换 a（在篮 1）和 b（在篮 2），直接换代价是 `min(a,b)`；
> 也可以**借 m 中转**：先用 m 换 a，再用 m 换 b，总代价 `2 * m`。

所以每一对的实际代价是 **`min(min(a, b), 2 * m)`**。
把它套进 ② 的「前一半之和」里：
```python
cost = sum(min(x, 2 * m) for x in sorted(extra1 + extra2)[:len(extra1)])
```

**漏掉 `2 * m` 这一项是本题最常见的错解。**

复杂度：**O(n log n)** 时间（排序主导），O(n) 空间。

边界：
  - 两篮已经相同 → 0
  - 某种水果总数为奇数 → -1
  - 全局最小值就在待换元素里（此时 `2*m` 不会更优，公式自动退化）
  - `basket1=[4,2,2,2], basket2=[1,4,1,2]` → 1
  - `basket1=[2,3,4,1], basket2=[3,2,5,1]` → -1
"""

from collections import Counter
from typing import List


##################################################################################################
##### ! Solution 1: 频率平衡 + 合并排序取前一半 + min(x, 2*全局最小)
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：「交换代价 = min(两者)」类题；核心是「借全局最小值中转」这个技巧
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minCost(self, basket1: List[int], basket2: List[int]) -> int:
        cnt = Counter(basket1) + Counter(basket2)
        if any(c % 2 for c in cnt.values()):
            return -1                               # ! 某种水果总数是奇数 ⟹ 平分不了
        c1, c2 = Counter(basket1), Counter(basket2)
        extra: List[int] = []
        for v, total in cnt.items():
            half = total // 2
            # ! 篮 1 多出来的部分（或篮 2 多出来的部分），都要参与交换
            extra.extend([v] * abs(c1[v] - half))
        extra.sort()
        m = min(min(basket1), min(basket2))         # ! 全局最小，可以当「中转」用
        # ! extra 的长度是偶数；只有一半需要付代价（另一半搭车）
        return sum(min(x, 2 * m) for x in extra[:len(extra) // 2])


##################################################################################################
##### ! Solution 2: 暴力 —— BFS 搜索最小交换代价（基准答案，用来对拍；只适合极小输入）
##### ! 时间复杂度: 指数级   空间复杂度: 指数级
##### ! 适用：正确性参照，特别是验证「借最小值中转」确实有时更便宜
##################################################################################################


class Solution_2:
    def minCost(self, basket1: List[int], basket2: List[int]) -> int:
        import heapq
        n = len(basket1)
        start = (tuple(sorted(basket1)), tuple(sorted(basket2)))
        if start[0] == start[1]:
            return 0
        best = {start: 0}
        pq = [(0, start)]
        while pq:
            cost, (b1, b2) = heapq.heappop(pq)
            if cost > best.get((b1, b2), float("inf")):
                continue
            if b1 == b2:
                return cost
            for i in range(n):
                for j in range(n):
                    if b1[i] == b2[j]:
                        continue
                    nb1 = tuple(sorted(b1[:i] + (b2[j],) + b1[i + 1:]))
                    nb2 = tuple(sorted(b2[:j] + (b1[i],) + b2[j + 1:]))
                    nc = cost + min(b1[i], b2[j])
                    if nc < best.get((nb1, nb2), float("inf")):
                        best[(nb1, nb2)] = nc
                        heapq.heappush(pq, (nc, (nb1, nb2)))
        return -1


if __name__ == "__main__":
    import random

    cases = [([4, 2, 2, 2], [1, 4, 1, 2], 1),
             ([2, 3, 4, 1], [3, 2, 5, 1], -1),
             ([1, 1], [1, 1], 0),
             ([1, 2], [2, 1], 0),
             ([5, 5, 1], [1, 5, 5], 0)]
    for b1, b2, want in cases:
        a = Solution_1().minCost(b1[:], b2[:])
        assert a == want, (b1, b2, a, want)
        print(f"{b1} / {b2} -> {a}")

    for _ in range(200):                 # ! 极小输入和 Dijkstra 暴力对拍
        n = random.randint(1, 3)
        pool = [random.randint(1, 5) for _ in range(n)]
        b1 = pool + [random.randint(1, 5) for _ in range(n)]
        # ! 构造一个必然可行的输入：让每种水果出现偶数次
        c = Counter(b1)
        b1 = []
        for v, k in c.items():
            b1.extend([v] * (k * 2))
        random.shuffle(b1)
        half = len(b1) // 2
        a_, b_ = b1[:half], b1[half:]
        if Counter(a_ + b_) != Counter(a_) + Counter(b_):
            continue
        g = Solution_1().minCost(a_[:], b_[:])
        if g == -1:
            continue
        e = Solution_2().minCost(a_[:], b_[:])
        assert g == e, (a_, b_, g, e)
    print("随机对拍通过 ✓（频率平衡贪心 == Dijkstra 暴力搜索最小交换代价）")
