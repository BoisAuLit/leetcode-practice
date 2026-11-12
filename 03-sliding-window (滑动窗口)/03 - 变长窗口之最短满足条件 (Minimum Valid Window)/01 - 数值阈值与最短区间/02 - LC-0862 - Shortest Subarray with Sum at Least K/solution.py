"""LC-0862 - Shortest Subarray with Sum at Least K

Level 1 · 03 最短满足条件 —— **当数组有负数时，普通滑动窗口失效**
题目在问：和 >= k 的最短连续子数组长度。**nums 可以有负数**（这是和 LC-0209 的唯一区别）

为什么 LC-0209 的两指针在这里是错的：
      209 靠的是「窗口变长 ⇒ 和不减」，于是左端可以单调右移、永不回退。
      有负数时这条断了：一个当前不够大的窗口，往右扩可能变小、再扩又变大，
      所以**不能因为当前窗口不合法就丢掉它的左端**。
      反例：`nums = [2, -1, 2], k = 3` —— 答案是整段 3，但 209 式收缩会先把 2 吐掉。

决定性观察（换一个视角）：令前缀和 `P[j] = nums[0..j-1]` 之和。
      区间 `[i, j)` 的和 >= k ⟺ `P[j] - P[i] >= k`。
      固定右端 j，要找**最大的** i 使 `P[i] <= P[j] - k`。

单调队列的两条删除规则（整道题就这两句）：
  1. **队首出队**：若 `P[queue[0]] <= P[j] - k`，则 `[queue[0], j)` 合法，
     用它更新答案并把队首弹掉 —— 因为再往后的 j 只会让这个区间更长，它已经没用了。
  2. **队尾出队**：若 `P[queue[-1]] >= P[j]`，弹掉队尾 ——
     j 比它更靠右、前缀和还更小，**它在任何未来都不可能比 j 更优**。
  两条规则让队列里的前缀和严格递增，每个下标进出各一次 ⇒ O(n)。

Loop Invariant：队列里的下标递增，且对应的 `P` 值严格递增。

坑：
  - 队列存的是**下标**不是值（要算长度）
  - 前缀和数组长度是 n+1，下标 0 代表空前缀，必须入队
  - 两个 while 的顺序：先处理队首（收答案），再处理队尾（维护单调），最后把 j 入队
  - 答案要用 `n + 1` 当哨兵初值，没找到返回 -1（注意 209 返回的是 0，这题是 -1）
"""

from collections import deque
from typing import List


##################################################################################################
##### ! Solution 1: 前缀和 + 单调递增队列
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：带负数的「最短和 >= k 区间」唯一的线性解；也是 LC-0239 单调队列思想的另一种用法
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        n = len(nums)
        P = [0] * (n + 1)
        for i, x in enumerate(nums):
            P[i + 1] = P[i] + x
        dq = deque()                     # 存下标，对应的 P 值严格递增
        best = n + 1
        for j in range(n + 1):
            while dq and P[j] - P[dq[0]] >= k:   # ! 规则 1：合法就收答案并弹队首
                best = min(best, j - dq.popleft())
            while dq and P[dq[-1]] >= P[j]:      # ! 规则 2：队尾不可能更优，弹掉
                dq.pop()
            dq.append(j)
        return best if best <= n else -1


##################################################################################################
##### ! Solution 2: 暴力枚举所有区间（基线）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(1)
##### ! 适用：对拍参照；n 到 1e5 必然超时，但它能直观说明「为什么不能贪心收缩左端」
##################################################################################################


class Solution_2:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        n = len(nums)
        best = n + 1
        for i in range(n):
            s = 0
            for j in range(i, n):
                s += nums[j]
                if s >= k:
                    best = min(best, j - i + 1)
                    break
        return best if best <= n else -1


if __name__ == "__main__":
    import random
    cases = [([1], 1, 1), ([1, 2], 4, -1), ([2, -1, 2], 3, 3),
             ([84, -37, 32, 40, 95], 167, 3), ([-28, 81, -20, 28, -29], 89, 3)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for nums, k, want in cases:
            got = sol.shortestSubarray(nums[:], k)
            assert got == want, f"{type(sol).__name__} {nums} k={k}: got {got}, want {want}"
    rng = random.Random(862)
    for _ in range(4000):
        nums = [rng.randint(-8, 8) for _ in range(rng.randint(1, 11))]
        k = rng.randint(-5, 20)
        want = Solution_2().shortestSubarray(nums[:], k)
        assert Solution_1().shortestSubarray(nums[:], k) == want, (nums, k, want)
    print("2 个解法全过（含 4000 组随机对拍，含负数与负 k）")
