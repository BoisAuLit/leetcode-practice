"""LC-0455 - Assign Cookies

Level 1 · 05 多序列同步扫描 —— 两个有序序列的**同向**贪心配对
题目在问：每个孩子有胃口 g[i]，每块饼干有尺寸 s[j]，一块饼干只能给一个孩子，
      `s[j] >= g[i]` 才算满足。最多能满足几个孩子

决定性观察：两边都排序后，**用最小的饼干去喂胃口最小的孩子**。
  - 如果最小的饼干能喂饱胃口最小的孩子 → 喂他（用更大的饼干喂他是浪费）
  - 如果喂不饱 → 这块饼干谁都喂不饱（他是胃口最小的），直接丢弃

循环不变量：`i` 指向还没被满足的最小胃口的孩子，`j` 指向还没用掉的最小饼干。
  每轮至少有一个指针前进，所以是 O(n + m) 轮（排序 O(n log n + m log m) 主导）。

正确性简证（交换论证）：设最优解用饼干 x 满足了孩子 i（胃口最小）。
  因为 `s[j] <= x` 且 `s[j] >= g[i]`，把 x 换成 s[j] 仍然可行，
  而把更大的 x 留给后面只会更好。所以「最小配最小」不会比最优解差。

和同类题的区别（这三种贪心双指针不要混）：
  - **455 同向**：两个序列各一个指针，都从小往大走，配对成功才双双前进
  - **881 对撞**：一个序列两个指针，最轻配最重，因为"最重的必须占一条船"
  - **088 归并**：不做决策，只是按大小把两个有序序列合起来

坑：
  - 排序别忘了，题目不保证有序
  - 循环条件是 `i < len(g) and j < len(s)`，任一方用尽就结束
  - 答案是被满足的孩子数（等于 i 的最终值），不是饼干数
"""

from typing import List


##################################################################################################
##### ! Solution 1: 双排序 + 同向双指针贪心
##### ! 时间复杂度: O(n log n + m log m)   空间复杂度: O(1) 额外
##### ! 适用：所有「两个有序集合做最大匹配 + 单调可行条件」的题；一眼就能套
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        g.sort()
        s.sort()
        i = j = 0
        while i < len(g) and j < len(s):
            if s[j] >= g[i]:   # ! 这块饼干够喂当前最小胃口的孩子 → 成交，两边都前进
                i += 1
            j += 1             # ! 不够的话这块饼干谁都喂不饱，丢掉
        return i


##################################################################################################
##### ! Solution 2: 从大到小配对（对称写法）
##### ! 时间复杂度: O(n log n + m log m)   空间复杂度: O(1) 额外
##### ! 适用：同一个贪心的另一个方向 —— 用最大的饼干喂胃口最大的孩子；用来验证贪心的对称性
##################################################################################################


class Solution_2:
    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        g.sort(reverse=True)
        s.sort(reverse=True)
        i = j = cnt = 0
        while i < len(g) and j < len(s):
            if s[j] >= g[i]:   # ! 最大的饼干能喂饱最大的胃口 → 成交
                cnt += 1
                j += 1
            i += 1             # ! 喂不饱 → 这个孩子谁都满足不了他，跳过
        return cnt


if __name__ == "__main__":
    import random
    cases = [([1, 2, 3], [1, 1], 1), ([1, 2], [1, 2, 3], 2), ([], [1], 0),
             ([1], [], 0), ([10, 9, 8, 7], [5, 6, 7, 8], 2)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for g, s, want in cases:
            got = sol.findContentChildren(g[:], s[:])
            assert got == want, f"{type(sol).__name__} {g} {s}: got {got}, want {want}"

    def brute(g, s):   # ! 二分图最大匹配的暴力版（枚举饼干的全排列太慢，用状压 DP）
        n, m = len(g), len(s)
        from functools import lru_cache
        G, S = tuple(sorted(g)), tuple(sorted(s))
        @lru_cache(maxsize=None)
        def go(i, mask):          # i = 处理到第 i 个孩子，mask = 哪些饼干已用
            if i == n:
                return 0
            best = go(i + 1, mask)                      # 不满足这个孩子
            for j in range(m):
                if not (mask >> j & 1) and S[j] >= G[i]:
                    best = max(best, 1 + go(i + 1, mask | (1 << j)))
            return best
        return go(0, 0)

    rng = random.Random(455)
    for _ in range(400):
        g = [rng.randint(1, 6) for _ in range(rng.randint(0, 5))]
        s = [rng.randint(1, 6) for _ in range(rng.randint(0, 5))]
        want = brute(g, s)
        for sol in sols:
            assert sol.findContentChildren(g[:], s[:]) == want, (type(sol).__name__, g, s, want)
    print("2 个解法全过（含 400 组随机对拍 vs 状压最大匹配）")
