"""LC-0974 - Subarray Sums Divisible by K

Level 1 · 03 Prefix Sum 与 Prefix-Suffix —— 前缀和取模 + 余数计数
题目在问：有多少个非空连续子数组，它们的和能被 k 整除

核心观察：`sum(i..j) = pre[j+1] - pre[i]`，它能被 k 整除
      ⟺ `pre[j+1] ≡ pre[i] (mod k)`，也就是**两端的前缀和同余**。
      于是问题变成：在所有前缀和的余数里，任取两个相同的，有多少种取法。

不变量：扫到位置 j 时，`cnt[r]` = 前面出现过多少个余数为 r 的前缀和（含哨兵 pre=0）。
      每遇到一个余数 r，就把 `cnt[r]` 加进答案，再 `cnt[r] += 1`。
      这等价于最后对每个余数算 C(m, 2)，但边扫边加只需要一遍。

和同层另外两题的区别：
  - 560：键是前缀和本身，问个数 → 存次数
  - 525：键是前缀和（0 换 -1），问最长 → 存第一次出现的下标
  - 974：键是前缀和的**余数**，问个数 → 存次数

坑：
  - `cnt[0] = 1` 的哨兵不能少，它代表「空前缀」，负责统计从头开始就整除的那些段
  - 负数取模：Python 的 `%` 结果恒非负（`-3 % 5 == 2`），**直接用就对**；
    C++/Java 的 `%` 会给出负余数，必须写成 `((x % k) + k) % k`，面试要主动说这一句
  - 答案可能很大（n 到 3e4 时约 4.5e8 对），Java/C++ 要注意 int 溢出
"""

from collections import defaultdict
from typing import List


##################################################################################################
##### ! Solution 1: 前缀和取模 + 余数计数，一遍扫完
##### ! 时间复杂度: O(n)   空间复杂度: O(k)
##### ! 适用：所有「区间和满足同余条件」的计数题；523 Continuous Subarray Sum 是同一个壳
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        cnt = defaultdict(int)
        cnt[0] = 1  # ! 哨兵：空前缀的余数是 0
        ans = pre = 0
        for x in nums:
            pre = (pre + x) % k  # ! Python 的 % 永远非负，不用额外修正
            ans += cnt[pre]      # ! 前面每一个同余的前缀，都和当前位置夹出一个合法子数组
            cnt[pre] += 1
        return ans


##################################################################################################
##### ! Solution 2: 先数每个余数有几个，再算组合数 C(m, 2)
##### ! 时间复杂度: O(n + k)   空间复杂度: O(k)
##### ! 适用：同一件事的「离线」写法；把「边扫边加」还原成组合计数，更容易向别人解释为什么对
##################################################################################################


class Solution_2:
    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        cnt = [0] * k
        cnt[0] = 1
        pre = 0
        for x in nums:
            pre = (pre + x) % k
            cnt[pre] += 1
        return sum(m * (m - 1) // 2 for m in cnt)  # ! 同余的 m 个前缀两两配对


##################################################################################################
##### ! Solution 3: 暴力枚举所有区间（基线）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(1)
##### ! 适用：对拍参照
##################################################################################################


class Solution_3:
    def subarraysDivByK(self, nums: List[int], k: int) -> int:
        ans = 0
        for i in range(len(nums)):
            s = 0
            for j in range(i, len(nums)):
                s += nums[j]
                if s % k == 0:
                    ans += 1
        return ans


if __name__ == "__main__":
    cases = [([4, 5, 0, -2, -3, 1], 5, 7), ([5], 9, 0), ([-1, 2, 9], 2, 2),
             ([0, 0, 0], 1, 6), ([-5, -5], 5, 3)]
    for sol in (Solution_1(), Solution_2(), Solution_3()):
        for nums, k, want in cases:
            got = sol.subarraysDivByK(nums[:], k)
            assert got == want, f"{type(sol).__name__} {nums} k={k}: got {got}, want {want}"
    print("3 个解法全过")
