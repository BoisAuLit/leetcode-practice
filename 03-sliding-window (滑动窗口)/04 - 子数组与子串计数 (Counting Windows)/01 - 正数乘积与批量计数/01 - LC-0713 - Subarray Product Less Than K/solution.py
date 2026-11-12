"""LC-0713 - Subarray Product Less Than K

Level 1 · 04 计数窗口 —— Counting Window（计数窗口）的入门题
题目在问：乘积严格小于 k 的连续子数组**有多少个**

决定性观察（计数窗口的核心公式）：
      维护一个合法窗口 `[left, right]`（乘积 < k）之后，
      **以 right 结尾的合法子数组恰好有 `right - left + 1` 个**：
      `[left..right]`、`[left+1..right]`、…、`[right..right]`。
      它们都是合法窗口的后缀，而合法窗口的后缀乘积只会更小（元素都是正数），所以必然合法。
      把每个 right 的贡献加起来就是答案 —— 一次加一批，不用逐个枚举。

这就是「计数窗口」和前两层的根本差别：
  - 最长合法：答案 = max(窗口长度)
  - 最短满足：答案 = min(窗口长度)
  - **计数**：答案 = Σ(每个 right 的合法起点个数)

正确性依赖 `nums[i] >= 1`：乘积随窗口变长单调不减，left 才能单调右移。
      有 0 或负数时这套就不成立（0 会让乘积恒为 0，负数让单调性消失）。

坑：
  - **`k <= 1` 必须直接返回 0**：乘积至少是 1（元素 >= 1），不可能 < 1；
    不特判的话内层 while 会把 left 推到 right+1，继而出现负数长度
  - 收缩用 while，且要守 `left <= right`
  - 条件是严格小于 k
"""

from typing import List


##################################################################################################
##### ! Solution 1: 变长窗口 + 一次加 right - left + 1
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：所有「统计满足单调约束的子数组个数」的题；1358、2762 都靠这条公式
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        if k <= 1:
            return 0                      # ! 必须特判，否则 left 会越过 right
        left = 0
        prod = 1
        ans = 0
        for right, x in enumerate(nums):
            prod *= x
            while prod >= k:              # ! 不合法就收缩
                prod //= nums[left]
                left += 1
            ans += right - left + 1       # ! 以 right 结尾的所有合法子数组，一次加完
        return ans


##################################################################################################
##### ! Solution 2: 对数转换 + 前缀和 + 二分
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：把乘积变成加法的通用技巧；这题有浮点精度风险，只作为思想记录，不建议面试写
##################################################################################################


class Solution_2:
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        if k <= 1:
            return 0
        import bisect, math
        EPS = 1e-9
        pre = [0.0]
        for x in nums:
            pre.append(pre[-1] + math.log(x))
        logk = math.log(k)
        ans = 0
        for right in range(1, len(pre)):
            # ! 找最小的 left 使 pre[right] - pre[left] < logk
            lo = bisect.bisect_right(pre, pre[right] - logk + EPS, 0, right)
            ans += right - lo
        return ans


if __name__ == "__main__":
    import random
    cases = [([10, 5, 2, 6], 100, 8), ([1, 2, 3], 0, 0), ([1, 1, 1], 2, 6),
             ([10], 10, 0), ([10], 11, 1)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for nums, k, want in cases:
            got = sol.numSubarrayProductLessThanK(nums[:], k)
            assert got == want, f"{type(sol).__name__} {nums} k={k}: got {got}, want {want}"
    rng = random.Random(713)
    for _ in range(2000):
        nums = [rng.randint(1, 9) for _ in range(rng.randint(0, 9))]
        k = rng.randint(0, 60)
        want = 0
        for i in range(len(nums)):
            p = 1
            for j in range(i, len(nums)):
                p *= nums[j]
                if p < k: want += 1
                else: break
        for sol in sols:
            assert sol.numSubarrayProductLessThanK(nums[:], k) == want, (type(sol).__name__, nums, k, want)
    print("2 个解法全过（含 2000 组随机对拍）")
