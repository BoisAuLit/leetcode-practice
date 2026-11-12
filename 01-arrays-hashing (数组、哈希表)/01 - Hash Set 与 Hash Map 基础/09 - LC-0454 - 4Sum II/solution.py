"""LC-0454 - 4Sum II

Level 1 · 01 Hash Set 与 Hash Map 基础 —— Meet in the Middle（折半 + 哈希配对）
题目在问：四个等长数组，各取一个数，有多少种下标组合使四数之和为 0

核心观察：四重循环是 O(n^4)。但等式可以拆成两半 ——
      `a + b + c + d == 0` ⟺ `(a + b) == -(c + d)`。
      先把左半边所有 `a + b` 的**出现次数**存进哈希表（O(n^2)），
      再枚举右半边每个 `c + d`，查 `-(c+d)` 出现过几次，累加。总共 O(n^2)。

不变量：`cnt[s]` = 左半边凑出和为 s 的下标对 (i, j) 的个数。
      因为统计的是**下标对**而不是值，重复的值天然被算了多次，不用去重。

为什么和 Two Sum 是同一招：Two Sum 是「枚举右边、查左边的补数」，
      这题只是把「一个数」换成「一对数」—— 哈希表换补数（complement lookup）的通用形态。

坑：
  - 这题问的是**下标组合数**，不是去重后的值组合，所以不能用 set
  - 和 15/18（3Sum、4Sum）完全不是一回事：那两题要去重、要排序 + 双指针；
    这题四个数组独立，反而更简单
  - 用 defaultdict 或 Counter，别用 dict 后忘了默认值
"""

from collections import Counter, defaultdict
from typing import List


##################################################################################################
##### ! Solution 1: 一张哈希表存 a+b 的次数，再枚举 c+d 查补数
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n^2)
##### ! 适用：所有能拆成「两半分别枚举」的等式；n=200 时 4e4 次操作，比 1.6e9 的暴力快 4 万倍
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def fourSumCount(self, nums1: List[int], nums2: List[int],
                     nums3: List[int], nums4: List[int]) -> int:
        cnt = defaultdict(int)
        for a in nums1:
            for b in nums2:
                cnt[a + b] += 1  # ! 存的是「下标对的个数」，所以重复值要累加而不是覆盖
        ans = 0
        for c in nums3:
            for d in nums4:
                ans += cnt[-(c + d)]  # ! 查补数，查不到自然是 0
        return ans


##################################################################################################
##### ! Solution 2: 左右各建一张 Counter，再对着乘
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n^2)
##### ! 适用：同一件事的对称写法；遍历较小的那张表可以再快一点，也更容易解释「为什么是乘法」
##################################################################################################


class Solution_2:
    def fourSumCount(self, nums1: List[int], nums2: List[int],
                     nums3: List[int], nums4: List[int]) -> int:
        ab = Counter(a + b for a in nums1 for b in nums2)
        cd = Counter(c + d for c in nums3 for d in nums4)
        # ! 左边和为 s 的有 ab[s] 对，右边和为 -s 的有 cd[-s] 对，乘法原理
        return sum(v * cd[-s] for s, v in ab.items())


##################################################################################################
##### ! Solution 3: 四重循环暴力（基线）
##### ! 时间复杂度: O(n^4)   空间复杂度: O(1)
##### ! 适用：对拍参照；n=200 时要 1.6e9 次，必然超时
##################################################################################################


class Solution_3:
    def fourSumCount(self, nums1: List[int], nums2: List[int],
                     nums3: List[int], nums4: List[int]) -> int:
        return sum(1 for a in nums1 for b in nums2 for c in nums3 for d in nums4
                   if a + b + c + d == 0)


if __name__ == "__main__":
    import random
    cases = [([1, 2], [-2, -1], [-1, 2], [0, 2], 2),
             ([0], [0], [0], [0], 1),
             ([1], [1], [1], [1], 0)]
    sols = [Solution_1(), Solution_2(), Solution_3()]
    for sol in sols:
        for a, b, c, d, want in cases:
            got = sol.fourSumCount(a[:], b[:], c[:], d[:])
            assert got == want, f"{type(sol).__name__}: got {got}, want {want}"
    rng = random.Random(454)
    for _ in range(500):
        n = rng.randint(1, 5)
        arrs = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(4)]
        want = Solution_3().fourSumCount(*[x[:] for x in arrs])
        for sol in sols:
            assert sol.fourSumCount(*[x[:] for x in arrs]) == want, (type(sol).__name__, arrs)
    print("3 个解法全过（含 500 组随机对拍）")
