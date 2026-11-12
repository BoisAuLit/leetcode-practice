"""LC-0904 - Fruit Into Baskets

Level 1 · 02 最长合法区间 —— At Most K Distinct（最多 K 种不同元素），这里 K = 2
题目在问：两个篮子各装一种水果，从某棵树开始连续采摘，最多能摘几个
      = **最长的、最多只含 2 种不同值的连续子数组**的长度

决定性观察：题面是果篮，实质是「最多 K 种 distinct」。
      **LC-0159（最多两种不同字符）和本题是同一个算法**，只是数组换成了字符串；
      LC-0340（最多 K 种）把 2 换成参数。三题一个模板，不要记三遍。

Window Expansion Rule：`right` 无条件前进，把 `fruits[right]` 加进频率表。
Window Shrinking Rule：**当且仅当窗口不合法**（`len(freq) > 2`）时收缩 left，
      直到重新合法。这是「最长合法窗口」这一族的共同形状 ——
      和「最短满足窗口」（LC-0209 / 0076）正好相反：那边是**合法时才收缩**。

Loop Invariant：每轮结束时 `[left, right]` 一定是合法窗口（distinct <= 2），
      并且它是以 `right` 结尾的最长合法窗口。所以答案就是所有轮里的最大长度。

正确性简证：left 只增不减。若某个 left 曾经可行，更小的 left 之后也不会再可行
（加入的元素只会让 distinct 变多，不会变少），所以不回退是安全的，总体 O(n)。

坑：
  - 计数归零一定要 `del`，否则 `len(freq)` 失真（和 LC-2461 同一个坑）
  - 收缩用 `while` 不是 `if`：虽然这题一次只会多出一种，但养成 while 的习惯
  - 返回的是长度，不是水果种类
"""

from collections import defaultdict
from typing import List

K = 2  # ! 篮子数；改成参数就是 LC-0340


##################################################################################################
##### ! Solution 1: 变长窗口 + 频率表，不合法就收缩
##### ! 时间复杂度: O(n)   空间复杂度: O(K)
##### ! 适用：At Most K Distinct 的通用模板（904 / 159 / 340 共用）
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def totalFruit(self, fruits: List[int]) -> int:
        freq = defaultdict(int)
        left = 0
        best = 0
        for right, x in enumerate(fruits):
            freq[x] += 1
            while len(freq) > K:              # ! 不合法才收缩
                out = fruits[left]
                freq[out] -= 1
                if freq[out] == 0:
                    del freq[out]
                left += 1
            best = max(best, right - left + 1)
        return best


##################################################################################################
##### ! Solution 2: 只记「每种水果最后出现的位置」（K 很小时的常数优化）
##### ! 时间复杂度: O(n)   空间复杂度: O(K)
##### ! 适用：K = 2 时可以不维护完整频率表：超出两种时，左端直接跳到「较早那种的最后位置 + 1」
##################################################################################################


class Solution_2:
    def totalFruit(self, fruits: List[int]) -> int:
        last = {}          # 水果 -> 最后一次出现的下标
        left = 0
        best = 0
        for right, x in enumerate(fruits):
            last[x] = right
            if len(last) > K:
                # ! 最后出现最早的那种水果，整段丢掉
                drop = min(last, key=last.get)
                left = last[drop] + 1
                del last[drop]
            best = max(best, right - left + 1)
        return best


if __name__ == "__main__":
    import random
    cases = [([1, 2, 1], 3), ([0, 1, 2, 2], 3), ([1, 2, 3, 2, 2], 4),
             ([3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4], 5), ([1], 1)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for f, want in cases:
            got = sol.totalFruit(f[:])
            assert got == want, f"{type(sol).__name__} {f}: got {got}, want {want}"
    rng = random.Random(904)
    for _ in range(3000):
        f = [rng.randint(0, 4) for _ in range(rng.randint(1, 14))]
        want = max(j - i + 1 for i in range(len(f)) for j in range(i, len(f))
                   if len(set(f[i:j + 1])) <= K)
        for sol in sols:
            assert sol.totalFruit(f[:]) == want, (type(sol).__name__, f, want)
    print("2 个解法全过（含 3000 组随机对拍）")
