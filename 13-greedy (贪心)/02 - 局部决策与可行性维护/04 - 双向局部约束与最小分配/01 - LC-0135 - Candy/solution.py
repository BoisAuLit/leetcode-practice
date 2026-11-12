"""LC-0135 - Candy

Level 1 · 02 局部决策与可行性维护 —— **双向约束 ⟹ 扫两遍**
题目在问：每个孩子至少 1 颗糖；**评分比邻居高的必须比那个邻居拿得多**。求最少总糖数。

决定性观察（本题的全部）：
  1. 约束是**双向的**：
     - `ratings[i] > ratings[i-1]` ⟹ `candy[i] > candy[i-1]`（看左边）
     - `ratings[i] > ratings[i+1]` ⟹ `candy[i] > candy[i+1]`（看右边）
  2. **一次扫描只能满足一个方向**。所以**扫两遍**：
     ```
     从左到右：只管「比左邻居高就比左邻居多」
     从右到左：只管「比右邻居高就比右邻居多」
     最后取 max(左结果, 右结果)
     ```
  3. **为什么取 max 就同时满足两个方向**：
     `left[i]` 满足了左约束，`right[i]` 满足了右约束。
     取 `max` 之后，两个约束**都仍然满足**（值只变大，不会破坏「比邻居多」这种下界约束），
     而且是满足两者的**最小**值 ⟹ 总和最小。
  4. 全部初始化为 1（每人至少 1 颗）。

```python
n = len(ratings)
left = [1] * n
for i in range(1, n):
    if ratings[i] > ratings[i-1]: left[i] = left[i-1] + 1
right = [1] * n
for i in range(n-2, -1, -1):
    if ratings[i] > ratings[i+1]: right[i] = right[i+1] + 1
return sum(max(l, r) for l, r in zip(left, right))
```

> **「双向约束 ⟹ 正反各扫一遍再取 max/min」是一个能直接复用的模式**：
> | 题 | 怎么用 |
> |---|---|
> | **LC-0135** 本题 | 左右各扫一遍取 max |
> | **LC-0042** Trapping Rain Water | 前缀最大、后缀最大，取 min |
> | **LC-0238** Product of Array Except Self | 前缀积、后缀积，相乘 |

**O(1) 空间的进阶解法**（Solution_2）：
一次扫描，维护「当前上坡长度」和「当前下坡长度」，
在坡顶处结算。思路巧但容易错，面试给两遍扫描版就够了。

复杂度：Solution_1 O(n) 时间 / **O(n) 空间**；Solution_2 O(n) / **O(1)**。

边界：
  - 严格递增 `[1,2,3]` → 1+2+3 = 6
  - 严格递减 `[3,2,1]` → 3+2+1 = 6
  - 全部相同 `[1,1,1]` → 3（相同不需要更多）
  - 单峰 `[1,3,2,2,1]` → 1+3+1+2+1? 实际 → 7
  - 单个孩子 → 1
"""

from typing import List


##################################################################################################
##### ! Solution 1: 左右各扫一遍，最后取 max
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：所有「双向邻居约束」的题；和 LC-0042、LC-0238 是同一个模式
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        if n == 0:
            return 0
        left = [1] * n                       # ! 只满足「看左边」的约束
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                left[i] = left[i - 1] + 1
        right = [1] * n                      # ! 只满足「看右边」的约束
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                right[i] = right[i + 1] + 1
        # ! 取 max 同时满足两个方向，而且是满足两者的最小值
        return sum(max(l, r) for l, r in zip(left, right))


##################################################################################################
##### ! Solution 2: 一次扫描 O(1) 空间（维护上坡/下坡长度，在坡顶结算）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：被追问 O(1) 空间时；思路巧但边界多，面试首选 Solution_1
##################################################################################################


class Solution_2:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        if n == 0:
            return 0
        total = 1
        up = down = peak = 0
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                up += 1
                down = 0
                peak = up                      # ! 记住坡顶的高度
                total += 1 + up
            elif ratings[i] == ratings[i - 1]:
                up = down = peak = 0
                total += 1                     # ! 相同 ⟹ 重新从 1 开始
            else:
                up = 0
                down += 1
                # ! 下坡：如果下坡比坡顶还长，坡顶要被抬高一格
                total += 1 + down - (1 if peak >= down else 0)
        return total


##################################################################################################
##### ! Solution 3: 反复松弛直到稳定（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2) 最坏   空间复杂度: O(n)
##### ! 适用：正确性参照 —— 直接按约束反复修正，一定收敛到最小可行解
##################################################################################################


class Solution_3:
    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        if n == 0:
            return 0
        c = [1] * n
        changed = True
        while changed:
            changed = False
            for i in range(n):
                if i > 0 and ratings[i] > ratings[i - 1] and c[i] <= c[i - 1]:
                    c[i] = c[i - 1] + 1
                    changed = True
                if i < n - 1 and ratings[i] > ratings[i + 1] and c[i] <= c[i + 1]:
                    c[i] = c[i + 1] + 1
                    changed = True
        return sum(c)


if __name__ == "__main__":
    import random

    cases = [([1, 0, 2], 5), ([1, 2, 2], 4), ([1, 2, 3], 6), ([3, 2, 1], 6),
             ([1, 1, 1], 3), ([1], 1), ([1, 3, 2, 2, 1], 7)]
    for r, want in cases:
        a = Solution_1().candy(r[:])
        b = Solution_2().candy(r[:])
        c = Solution_3().candy(r[:])
        assert a == b == c == want, (r, a, b, c, want)
        print(f"{r} -> {a}")

    for _ in range(1000):                # ! 小值域随机对拍，专压相同评分和长下坡
        r = [random.randint(0, 3) for _ in range(random.randint(0, 12))]
        a = Solution_1().candy(r[:])
        b = Solution_2().candy(r[:])
        c = Solution_3().candy(r[:])
        assert a == b == c, (r, a, b, c)
    print("随机对拍 1000 组通过 ✓（两遍扫描 == 一次扫描 O(1) == 反复松弛）")
