"""LC-0004 - Median of Two Sorted Arrays

Level 1 · 05 双有序数组与分区二分 —— Binary Search on Partition（对分区位置二分）
题目在问：两个有序数组的中位数，要求 O(log(m+n))。

（本文件的 Solution_1 是**原 NeetCode 目录里用户已有的实现**，一字未改，只是加了标题注释。）

决定性观察：
  1. 中位数的本质是**把两个数组合起来切成左右两半**，使：
        - 左半的元素个数 = (m + n + 1) // 2
        - 左半的每个元素 <= 右半的每个元素
     只要找到这个切法，答案就能 O(1) 算出来，根本不需要真的合并数组。
  2. 两个数组的切点**不是独立的**：
     在 A 里切了 i 个（A[0..i-1] 归左半），那 B 里必须切 `half - i` 个。
     所以**只有一个自由变量** —— 这正是能二分的原因。
  3. 正确切分的判据只有两条（交叉比较）：
        `Aleft <= Bright`  且  `Bleft <= Aright`
     - 若 `Aleft > Bright`：A 切多了 → 往左移（`r = i - 1`）
     - 若 `Bleft > Aright`：A 切少了 → 往右移（`l = i + 1`）

为什么只需要在**较短**的数组上二分：
      切点 j = half - i 必须落在 `[0, len(B)]` 内。若在较长数组上二分，
      j 可能越界，还要额外处理。先 swap 保证 `len(A) <= len(B)`，j 自动合法。
      复杂度也因此是 **O(log(min(m, n)))**，比 O(log(m+n)) 更好。

±infinity 哨兵的作用：
      切点在最左（i == 0）时没有 Aleft，用 `-inf` 表示「左边界无穷小，永远 <= 任何数」；
      切点在最右（i == len(A)）时没有 Aright，用 `+inf`。
      有了哨兵，**空数组和边界切点都不需要单独写分支**，这是这份实现最漂亮的地方。

奇偶怎么算：
      `half = (m + n) // 2`，本实现里左半取 `half` 个（见 `j = half - i - 2` 的下标约定）。
      - 总长为奇数 → 中位数 = `min(Aright, Bright)`
      - 总长为偶数 → 中位数 = `(max(Aleft, Bleft) + min(Aright, Bright)) / 2`

复杂度：O(log(min(m, n))) 时间，O(1) 空间。

本题是 Hard，标记 **P1 进阶**：
      先把 Level 1 的 01–03 全部吃透再来，不要在入门阶段硬背这份代码。

边界：
  - nums1=[1,3], nums2=[2] → 2.0
  - nums1=[1,2], nums2=[3,4] → 2.5
  - 其中一个为空
  - 两个数组值域完全不重叠（[1,2] 和 [100,200]）
  - 含重复元素
"""

from typing import List


##################################################################################################
##### ! Solution 1: 在较短数组上二分分区位置（用户原有实现，保持不变）
##### ! 时间复杂度: O(log(min(m, n)))   空间复杂度: O(1)
##### ! 适用：两个有序数组求第 k 小 / 中位数；±inf 哨兵免去所有边界分支
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findMedianSortedArrays(
        self, nums1: List[int], nums2: List[int]
    ) -> float:
        A, B = nums1, nums2
        total = len(nums1) + len(nums2)
        half = total // 2

        if len(B) < len(A):
            A, B = B, A

        l, r = 0, len(A) - 1
        while True:
            i = (l + r) // 2
            j = half - i - 2

            Aleft = A[i] if i >= 0 else float("-infinity")
            Aright = A[i + 1] if (i + 1) < len(A) else float("infinity")
            Bleft = B[j] if j >= 0 else float("-infinity")
            Bright = B[j + 1] if (j + 1) < len(B) else float("infinity")

            if Aleft <= Bright and Bleft <= Aright:
                if total % 2:
                    return min(Aright, Bright)
                return (max(Aleft, Bleft) + min(Aright, Bright)) / 2
            elif Aleft > Bright:
                r = i - 1
            else:
                l = i + 1


##################################################################################################
##### ! Solution 2: 合并两个有序数组后直接取中位数（基准答案，用来对拍）
##### ! 时间复杂度: O(m + n)   空间复杂度: O(m + n)
##### ! 适用：正确性参照；面试里可以先说这版，再被追问 O(log) 时给出 Solution_1
##################################################################################################


class Solution_2:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        merged = sorted(nums1 + nums2)       # ! 真正归并也行，这里求简洁
        n = len(merged)
        if n % 2:
            return float(merged[n // 2])
        return (merged[n // 2 - 1] + merged[n // 2]) / 2


if __name__ == "__main__":
    import random

    cases = [([1, 3], [2]), ([1, 2], [3, 4]), ([], [1]), ([2], []),
             ([1, 2], [100, 200]), ([1, 1, 1], [1, 1])]
    for a, b in cases:
        r = Solution_1().findMedianSortedArrays(a, b)
        assert abs(r - Solution_2().findMedianSortedArrays(a, b)) < 1e-9, (a, b)
        print(f"{a} + {b} -> {r}")

    for _ in range(1000):                # ! 随机对拍，含空数组与重复元素
        a = sorted(random.randint(0, 9) for _ in range(random.randint(0, 6)))
        b = sorted(random.randint(0, 9) for _ in range(random.randint(0, 6)))
        if not a and not b:
            continue
        r1 = Solution_1().findMedianSortedArrays(a, b)
        r2 = Solution_2().findMedianSortedArrays(a, b)
        assert abs(r1 - r2) < 1e-9, (a, b, r1, r2)
    print("随机对拍 1000 组通过 ✓")
