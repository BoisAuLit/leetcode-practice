"""LC-2537 - Count the Number of Good Subarrays

Level 1 · 04 子数组与子串计数 → Level 2 · 02 Exactly K 与 At Most K

题目在问：数一数有多少子数组里「相等数对 (i, j)，i < j，nums[i] == nums[j]」的个数 **≥ k**。

### 两个观察

1. **单调性**：子数组越长，相等数对只会越多（加元素不会减少数对）⟹ 「至少 k」是**单调谓词**，可以用滑动窗口。
2. **增量计算数对数**：值 x 进窗口时，新增的数对数 = 窗口里已有的 x 的个数 `cnt[x]`；x 出窗口时减少 `cnt[x] − 1`。
   不需要重新数，O(1) 更新。

### 「至少 k」的计数模板（和「至多 k」镜像）

    for r:  加入 nums[r]，pairs += cnt[x]; cnt[x] += 1
            while pairs >= k:  res += n − r      # ! 以 l 为左端、右端在 [r, n−1] 的全部合法 —— 右端再长只会更合法
                               移出 nums[l]
    「至多」模板是：while 不合法时收缩，然后 res += r − l + 1（左端在 [l, r] 的全部合法）
    「至少」模板是：while 合法时就收缩并计数 res += n − r（右端在 [r, n−1] 的全部合法）

两者的差别就是「合法集合在哪一侧是向外扩展的」。LC-2962 用的是同一个「至少」模板。
"""
from collections import defaultdict
from typing import List


##################################################################################################
##### ! Solution 1: 「至少 k」滑动窗口 + 数对数增量维护
##### ! 时间复杂度: O(n)   空间复杂度: O(不同值的个数)
##### ! 适用：面试标准答案。while pairs >= k 时 res += n − r 再移出左端
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def countGood(self, nums: List[int], k: int) -> int:
        cnt = defaultdict(int)
        n = len(nums)
        l = pairs = res = 0
        for r, x in enumerate(nums):
            pairs += cnt[x]; cnt[x] += 1                # ! x 和窗口里已有的每个 x 各成一对
            while pairs >= k:                           # ! 以 l 开头、r 结尾已经合法 → 右端再延长都合法
                res += n - r
                cnt[nums[l]] -= 1; pairs -= cnt[nums[l]]; l += 1   # ! 移出 nums[l]：少掉它和剩下同值元素的数对
        return res


##################################################################################################
##### ! Solution 2: 总数 − 「数对 < k」的子数组数（至多模板的补集）
##### ! 时间复杂度: O(n)   空间复杂度: O(不同值的个数)
##### ! 适用：展示 at_least(k) = total − at_most(k − 1)；at_most 用「不合法就收缩、res += r − l + 1」模板
##################################################################################################


class Solution_2:
    def countGood(self, nums: List[int], k: int) -> int:
        n = len(nums)
        cnt = defaultdict(int)
        l = pairs = at_most = 0                         # ! at_most：数对数 <= k−1 的子数组个数
        for r, x in enumerate(nums):
            pairs += cnt[x]; cnt[x] += 1
            while pairs > k - 1:                        # ! 不合法（数对 >= k）就收缩
                cnt[nums[l]] -= 1; pairs -= cnt[nums[l]]; l += 1
            at_most += r - l + 1
        return n * (n + 1) // 2 - at_most


##################################################################################################
##### ! Solution 3: 暴力 O(n²)（真值基线）
##### ! 时间复杂度: O(n²)   空间复杂度: O(n)
##### ! 适用：只用来对拍；固定左端向右扩，数对数增量累加
##################################################################################################


class Solution_3:
    def countGood(self, nums: List[int], k: int) -> int:
        n, res = len(nums), 0
        for i in range(n):
            cnt = defaultdict(int); pairs = 0
            for j in range(i, n):
                pairs += cnt[nums[j]]; cnt[nums[j]] += 1
                if pairs >= k:
                    res += 1
        return res


if __name__ == "__main__":
    import random
    cases = [([1, 1, 1, 1, 1], 10, 1), ([3, 1, 4, 3, 2, 2, 4], 2, 4), ([1], 1, 0), ([1, 1], 1, 1)]
    for nums, k, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().countGood(nums, k)
            assert got == want, (cls.__name__, nums, k, got, want)
    rng = random.Random(2537)
    for _ in range(4000):
        nums = [rng.randint(1, 3) for _ in range(rng.randint(1, 12))]
        k = rng.randint(1, 8)
        outs = [cls().countGood(nums, k) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (nums, k, outs)
    print("所有测试通过 ✓")
