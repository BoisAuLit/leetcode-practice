"""LC-1343 - Number of Sub-arrays of Size K and Average Greater than or Equal to Threshold

Level 1 · 01 定长窗口与频率匹配 → Level 2 · 01 数值聚合与固定窗口优化

题目在问：数一数有多少**长度恰好 k** 的子数组，平均值 ≥ threshold。

### 两个小技巧，全是这一层的基本功

1. **不要算平均值**：`sum / k >= threshold ⟺ sum >= threshold * k`。整数比较没有浮点误差，还少一次除法。
2. **定长窗口的滑动**：`window += nums[r] − nums[r − k]`，每步 O(1)；前 k−1 步只进不出。
   写法上把「进」放循环开头、「出」用 `if r >= k`、「判定」用 `if r >= k − 1`，三件事顺序不能乱。

### 另两种写法

- 前缀和：`P[r+1] − P[r+1−k]`，适合**多种长度**要反复查询时；单一长度用滑窗更省空间。
- `zip` 偏移：`for a, b in zip(nums, nums[k:])` 一边加 b 一边减 a，Pythonic 的定长窗口写法，面试里当彩蛋。
"""
from itertools import accumulate
from typing import List


##################################################################################################
##### ! Solution 1: 定长滑动窗口 + 整数比较 sum >= threshold * k
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：面试标准答案；定长窗口模板的最简实例
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def numOfSubarrays(self, arr: List[int], k: int, threshold: int) -> int:
        target = threshold * k                          # ! 平均 >= t ⟺ 和 >= t·k
        window = res = 0
        for r, x in enumerate(arr):
            window += x                                 # ! 进
            if r >= k:
                window -= arr[r - k]                    # ! 出（窗口满了之后）
            if r >= k - 1 and window >= target:         # ! 判定（窗口长度恰好 k）
                res += 1
        return res


##################################################################################################
##### ! Solution 2: 前缀和
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：若之后还要查别的长度 / 别的区间时，前缀和一次构造多次使用
##################################################################################################


class Solution_2:
    def numOfSubarrays(self, arr: List[int], k: int, threshold: int) -> int:
        P = [0] + list(accumulate(arr))                 # ! P[i] = arr[:i] 的和
        target = threshold * k
        return sum(1 for i in range(k, len(P)) if P[i] - P[i - k] >= target)


##################################################################################################
##### ! Solution 3: zip 偏移写法（Pythonic 定长窗口）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)（不算切片；arr[k:] 是视图语义的拷贝，严格说 O(n)）
##### ! 适用：面试彩蛋：先算第一个窗口，然后 zip(arr, arr[k:]) 同时给出「出」和「进」的元素
##################################################################################################


class Solution_3:
    def numOfSubarrays(self, arr: List[int], k: int, threshold: int) -> int:
        target = threshold * k
        window = sum(arr[:k])
        res = int(window >= target)
        for out_x, in_x in zip(arr, arr[k:]):           # ! out_x = arr[i], in_x = arr[i+k]
            window += in_x - out_x
            res += window >= target
        return res


def _brute(arr, k, t):
    return sum(1 for i in range(len(arr) - k + 1) if sum(arr[i:i + k]) / k >= t)


if __name__ == "__main__":
    import random
    cases = [([2, 2, 2, 2, 5, 5, 5, 8], 3, 4, 3), ([11, 13, 17, 23, 29, 31, 7, 5, 2, 3], 3, 5, 6), ([1], 1, 1, 1), ([1], 1, 2, 0)]
    for arr, k, t, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().numOfSubarrays(arr, k, t)
            assert got == want, (cls.__name__, arr, k, t, got, want)
    rng = random.Random(1343)
    for _ in range(4000):
        arr = [rng.randint(1, 10) for _ in range(rng.randint(1, 12))]
        k = rng.randint(1, len(arr)); t = rng.randint(1, 10)
        want = _brute(arr, k, t)
        for cls in (Solution_1, Solution_2, Solution_3):
            assert cls().numOfSubarrays(arr, k, t) == want, (cls.__name__, arr, k, t)
    print("所有测试通过 ✓")
