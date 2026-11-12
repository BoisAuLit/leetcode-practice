"""LC-0658 - Find K Closest Elements

Level 1 · 02 结构性二分 —— 对**连续窗口的起点**做二分
题目在问：有序数组里找最接近 x 的 k 个数，按升序返回；
         距离相同时**选更小的那个**（这条规则是全题的关键）。

决定性观察：
  1. 答案一定是一个**连续的子数组**（长度 k）。
     理由：数组有序，若答案里跳过了中间某个元素去取更远的，一定不会更优。
     这一步想通了，问题就从「选 k 个元素」变成了「选一个起点」。
  2. 于是只需要在起点 `i ∈ [0, n-k]` 上二分。
  3. 比较规则：对候选起点 mid，比较窗口**左端外侧**与**右端**：
         `x - arr[mid]`  vs  `arr[mid + k] - x`
     - 若 `x - arr[mid] > arr[mid+k] - x`：说明右边那个更近，窗口应该右移 → `lo = mid + 1`
     - 否则 → `hi = mid`
     用 `>` 而不是 `>=`，正好实现了「距离相等时取更小的那个」。

为什么比较的是 `arr[mid]` 和 `arr[mid+k]`：
      窗口 `[mid, mid+k-1]` 和 `[mid+1, mid+k]` 的区别只在于
      **丢掉 arr[mid]、换进 arr[mid+k]**。所以只要比较这两个元素谁离 x 更近就行，
      中间那 k-1 个元素两个窗口都有，不影响比较。

Loop Invariant：最优起点一定落在 `[lo, hi]` 内。
      注意这里 `hi` 的初值是 `n - k`（最右合法起点），不是 `n - 1`。

复杂度：**O(log(n-k) + k)** 时间（二分 + 切片），O(1) 额外空间（不算输出）。
      注意不是 O(log n)：最后还要输出 k 个元素。

边界：
  - arr=[1,2,3,4,5], k=4, x=3 → [1,2,3,4]
  - arr=[1,2,3,4,5], k=4, x=-1 → [1,2,3,4]（x 在左侧之外）
  - arr=[1,2,3,4,5], k=4, x=9 → [2,3,4,5]（x 在右侧之外）
  - k == n → 整个数组
  - 距离相等：arr=[1,3], k=1, x=2 → [1]（取更小的）
"""

from typing import List


##################################################################################################
##### ! Solution 1: 在窗口起点上二分
##### ! 时间复杂度: O(log(n-k) + k)   空间复杂度: O(1) 额外
##### ! 适用：答案是「定长连续窗口」且窗口优劣单调时；比双指针收缩更能体现二分边界思想
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        lo, hi = 0, len(arr) - k          # ! 起点的合法范围是 [0, n-k]
        while lo < hi:
            mid = (lo + hi) // 2
            # ! 严格大于才右移 → 距离相等时保留左边（题目要求取更小的）
            if x - arr[mid] > arr[mid + k] - x:
                lo = mid + 1
            else:
                hi = mid
        return arr[lo:lo + k]


##################################################################################################
##### ! Solution 2: 双指针从两端向内收缩，每次丢掉更远的那一端
##### ! 时间复杂度: O(n - k)   空间复杂度: O(1) 额外
##### ! 适用：最直观的写法；n 和 k 差距很大时比 Solution_1 慢
##################################################################################################


class Solution_2:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        lo, hi = 0, len(arr) - 1
        while hi - lo + 1 > k:
            # ! 距离相等时丢右边（保留更小的），和二分版的 tie-break 保持一致
            if x - arr[lo] <= arr[hi] - x:
                hi -= 1
            else:
                lo += 1
        return arr[lo:hi + 1]


##################################################################################################
##### ! Solution 3: 按 (|v - x|, v) 排序取前 k 个再排序（基准答案，用来对拍）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：正确性参照；排序键里带上 v 本身正好表达了「距离相同取更小」
##################################################################################################


class Solution_3:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        return sorted(sorted(arr, key=lambda v: (abs(v - x), v))[:k])


if __name__ == "__main__":
    import random

    cases = [([1, 2, 3, 4, 5], 4, 3), ([1, 2, 3, 4, 5], 4, -1), ([1, 2, 3, 4, 5], 4, 9),
             ([1, 3], 1, 2), ([1, 1, 1, 10, 10, 10], 1, 9), ([1], 1, 1)]
    for arr, k, x in cases:
        a = Solution_1().findClosestElements(arr, k, x)
        assert a == Solution_2().findClosestElements(arr, k, x), (arr, k, x)
        assert a == Solution_3().findClosestElements(arr, k, x), (arr, k, x, a)
        print(f"arr={arr}, k={k}, x={x} -> {a}")

    for _ in range(1000):                # ! 随机对拍，含重复元素与各种 x 位置
        n = random.randint(1, 10)
        arr = sorted(random.randint(0, 12) for _ in range(n))
        k = random.randint(1, n)
        x = random.randint(-2, 14)
        a = Solution_1().findClosestElements(arr, k, x)
        assert a == Solution_2().findClosestElements(arr, k, x) == Solution_3().findClosestElements(arr, k, x), (arr, k, x)
    print("随机对拍 1000 组通过 ✓")
