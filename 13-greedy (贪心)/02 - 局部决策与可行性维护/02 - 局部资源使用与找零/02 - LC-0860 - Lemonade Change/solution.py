"""LC-0860 - Lemonade Change

Level 1 · 02 局部决策与可行性维护 —— **优先用大面额找零**
题目在问：每人付 5/10/20，柠檬水 5 元。按顺序服务，能否给每个人正确找零？

决定性观察（贪心策略 + 为什么对）：
  1. 只需要记两个计数器：手上有几张 **5** 和几张 **10**（20 元永远找不出去，不用记）。
  2. 三种情况：
     - 付 5 ⟹ `five += 1`，不用找零
     - 付 10 ⟹ 找 5 ⟹ 需要 `five >= 1`
     - 付 20 ⟹ 找 15 ⟹ **优先用 `10 + 5`**，不够才用 `5 + 5 + 5`
  3. **为什么付 20 时要优先用 10 + 5**（交换论证）：
     10 元**只能**用来给付 20 的人找零；
     而 5 元**既能**给付 10 的人找零、**也能**给付 20 的人找零。
     ⟹ **5 元更"通用"，应该尽量留着** ⟹ 能用 10 就先用 10。
     这就是贪心成立的全部理由。

```python
five = ten = 0
for b in bills:
    if b == 5:   five += 1
    elif b == 10:
        if not five: return False
        five -= 1; ten += 1
    else:                                  # b == 20
        if ten and five:   ten -= 1; five -= 1     # ★ 优先 10 + 5
        elif five >= 3:    five -= 3
        else:              return False
return True
```

**不需要记 20 的张数** —— 它永远不会被当成找零发出去。
很多人多记一个 `twenty` 变量，虽然不错但没用。

> **本章的共同主题**：维护一个「资源状态」，每一步做局部决策，并证明
> 「优先消耗更不通用的资源」是最优的。
> LC-0135 Candy、LC-0605 Can Place Flowers 都在练同一件事。

复杂度：**O(n) 时间、O(1) 空间**。

边界：
  - 第一个人就付 10 或 20 → False
  - 全是 5 → True
  - `[5,5,5,10,20]` → True（20 用 10+5）
  - `[5,5,10,10,20]` → False（20 要 15，只有一张 5 和两张 10 ⟹ 10+5 后剩一张 10 没用）
  - 空数组 → True
"""

from typing import List


##################################################################################################
##### ! Solution 1: 两个计数器 + 「付 20 时优先用 10 + 5」
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：所有「维护资源状态 + 优先消耗不通用资源」的贪心
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def lemonadeChange(self, bills: List[int]) -> bool:
        five = ten = 0                # ! 20 元永远找不出去，不用记
        for b in bills:
            if b == 5:
                five += 1
            elif b == 10:
                if not five:
                    return False
                five -= 1
                ten += 1
            else:                                  # b == 20，要找 15
                if ten and five:                   # ! 优先 10 + 5：5 元更通用，留着
                    ten -= 1
                    five -= 1
                elif five >= 3:
                    five -= 3
                else:
                    return False
        return True


##################################################################################################
##### ! Solution 2: 暴力搜索所有找零方式（基准答案，用来对拍；验证贪心不会错）
##### ! 时间复杂度: 指数级   空间复杂度: 指数级
##### ! 适用：正确性参照 —— 它会尝试「付 20 时用 5+5+5」等所有分支
##################################################################################################


class Solution_2:
    def lemonadeChange(self, bills: List[int]) -> bool:
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dfs(i: int, five: int, ten: int) -> bool:
            if i == len(bills):
                return True
            b = bills[i]
            if b == 5:
                return dfs(i + 1, five + 1, ten)
            if b == 10:
                return five >= 1 and dfs(i + 1, five - 1, ten + 1)
            # ! b == 20：两种找零方式都试
            ok = False
            if ten >= 1 and five >= 1:
                ok = ok or dfs(i + 1, five - 1, ten - 1)
            if not ok and five >= 3:
                ok = ok or dfs(i + 1, five - 3, ten)
            return ok

        r = dfs(0, 0, 0)
        dfs.cache_clear()
        return r


if __name__ == "__main__":
    import random

    # ! [5,5,5,5,20,20] 的答案是 False：四张 5 只够给第一个 20 找零（5+5+5），第二个 20 就没钱了
    cases = [([5, 5, 5, 10, 20], True), ([5, 5, 10, 10, 20], False),
             ([10], False), ([5], True), ([], True),
             ([5, 5, 5, 5, 20, 20], False),
             ([5, 5, 10, 20, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5, 20, 5, 20, 5], True)]
    for bills, want in cases:
        a = Solution_1().lemonadeChange(bills[:])
        b = Solution_2().lemonadeChange(tuple(bills))
        assert a == b == want, (bills, a, b, want)
        print(f"{bills} -> {a}")

    for _ in range(1500):                # ! 随机对拍：贪心 == 穷举所有找零方式
        bills = [random.choice([5, 5, 10, 20]) for _ in range(random.randint(0, 12))]
        a = Solution_1().lemonadeChange(bills[:])
        b = Solution_2().lemonadeChange(tuple(bills))
        assert a == b, (bills, a, b)
    print("随机对拍 1500 组通过 ✓（贪心「优先 10+5」== 穷举所有找零分支）")
