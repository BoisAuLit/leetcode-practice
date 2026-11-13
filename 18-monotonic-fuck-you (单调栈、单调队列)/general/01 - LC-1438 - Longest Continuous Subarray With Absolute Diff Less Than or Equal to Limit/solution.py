"""LC-1438 - Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit

Level 1 · 05 单调队列与窗口极值 —— 变长窗口 + 两个 Monotonic Deque（单调双端队列）
题目在问：最长的连续子数组，使其中**任意两个元素之差的绝对值 <= limit**

决定性观察：
  1. 「任意两个元素之差 <= limit」⟺ **`max(window) - min(window) <= limit`**，
     只需要盯住极值，不需要两两比较。
  2. 窗口的极值不能像和那样 O(1) 增量维护（移除最大值后，新的最大值是谁？），
     所以要额外维护两个单调队列：
     - **递减队列**，队首是窗口最大值
     - **递增队列**，队首是窗口最小值

为什么队尾可以直接弹：新元素 x 进来时，队尾那些 `<= x` 的元素（对最大值队列而言）
      **在任何未来的窗口里都不可能再成为最大值** —— x 比它们大、又比它们活得久。
      这条「更年轻且更优 ⇒ 老的永远出局」的论证，和 LC-0239、LC-0862 是同一个。

Loop Invariant：两个队列里存的是**下标**，且下标递增；
      `maxq` 对应的值单调不增、`minq` 对应的值单调不减；
      队首下标 >= left（离开窗口的要及时弹掉）。

Window Shrinking Rule：`maxq[0] - minq[0] > limit` 时 left 右移一格，
      并把恰好等于 left-1 的队首弹掉。注意这里**一次只移一格**然后重新判断。

坑：
  - 队列存下标不存值：否则没法判断元素有没有离开窗口
  - 收缩时「谁的队首等于被移出的下标就弹谁」，两个队列都要检查
  - 队尾弹出用 `<=` 还是 `<` 都能过（相等的保留与否不影响极值），但要前后一致
  - 这道题也可以用 SortedList / 两个堆 + 懒删除做，复杂度 O(n log n)，单调队列是 O(n)
"""

from collections import deque
from typing import List


##################################################################################################
##### ! Solution 1: 变长窗口 + 两个单调队列（最大队列 + 最小队列）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：窗口里要同时盯住 max 和 min 的题；LC-0239 的自然进阶
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        maxq: deque[int] = deque()   # 下标，对应值单调不增 → 队首是最大值
        minq: deque[int] = deque()   # 下标，对应值单调不减 → 队首是最小值
        left = 0
        best = 0
        for right, x in enumerate(nums):
            while maxq and nums[maxq[-1]] <= x:
                maxq.pop()           # ! 比 x 小又比 x 老，永远不可能再当最大值
            maxq.append(right)
            while minq and nums[minq[-1]] >= x:
                minq.pop()
            minq.append(right)
            while nums[maxq[0]] - nums[minq[0]] > limit:   # ! 不合法就收缩
                if maxq[0] == left:
                    maxq.popleft()
                if minq[0] == left:
                    minq.popleft()
                left += 1
            best = max(best, right - left + 1)
        return best


##################################################################################################
##### ! Solution 2: 有序多重集合（SortedList 的手写替代：两个堆 + 懒删除）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：想不起单调队列时的退路；也是「窗口内要查第 k 小」这类更难问题的通用工具
##################################################################################################


class Solution_2:
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        import heapq
        maxh: List[tuple] = []   # (-值, 下标)
        minh: List[tuple] = []   # (值, 下标)
        left = 0
        best = 0
        for right, x in enumerate(nums):
            heapq.heappush(maxh, (-x, right))
            heapq.heappush(minh, (x, right))
            while -maxh[0][0] - minh[0][0] > limit:
                left += 1
                while maxh[0][1] < left:    # ! 懒删除：堆顶已经离开窗口才丢
                    heapq.heappop(maxh)
                while minh[0][1] < left:
                    heapq.heappop(minh)
            best = max(best, right - left + 1)
        return best


if __name__ == "__main__":
    import random
    cases = [([8, 2, 4, 7], 4, 2), ([10, 1, 2, 4, 7, 2], 5, 4),
             ([4, 2, 2, 2, 4, 4, 2, 2], 0, 3), ([1], 0, 1), ([1, 5], 100, 2)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for nums, lim, want in cases:
            got = sol.longestSubarray(nums[:], lim)
            assert got == want, f"{type(sol).__name__} {nums} limit={lim}: got {got}, want {want}"
    rng = random.Random(1438)
    for _ in range(3000):
        nums = [rng.randint(0, 12) for _ in range(rng.randint(1, 11))]
        lim = rng.randint(0, 8)
        want = max(j - i + 1 for i in range(len(nums)) for j in range(i, len(nums))
                   if max(nums[i:j + 1]) - min(nums[i:j + 1]) <= lim)
        for sol in sols:
            assert sol.longestSubarray(nums[:], lim) == want, (type(sol).__name__, nums, lim, want)
    print("2 个解法全过（含 3000 组随机对拍）")
