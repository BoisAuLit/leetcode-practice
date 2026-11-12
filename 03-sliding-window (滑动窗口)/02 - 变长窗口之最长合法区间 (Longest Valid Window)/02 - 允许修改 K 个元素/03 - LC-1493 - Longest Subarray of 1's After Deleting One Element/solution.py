"""LC-1493 - Longest Subarray of 1's After Deleting One Element

Level 1 · 02 变长窗口之最长合法区间 → Level 2 · 02 允许修改 K 个元素

题目在问：0/1 数组，**必须删掉一个元素**，求删后最长的全 1 子数组。

### 这就是 LC-1004（最多翻转 K 个 0）在 K = 1 时的版本，外加一个「必须删一个」

窗口内最多允许 1 个 0：`while zeros > 1: 左指针右移`。窗口长度 − 1 就是「删掉窗口里那个 0（或任意一个 1）」之后的全 1 长度。
**必须删一个**由 `− 1` 自动处理：全是 1 的数组 `[1,1,1]` 窗口长 3，答案 2 ✓ —— 不需要特判。

### 三种等价写法

| 写法 | 维护什么 | 适合 |
|---|---|---|
| 滑动窗口（K=1 的 1004 模板） | 窗口内 0 的个数 | 直接套模板，可推广到任意 K |
| 两段计数 `prev, cur` | 上一段连续 1 的长度和当前段 | O(1) 空间、一遍、无显式窗口；专属于 K=1 |
| 左右前缀 | `left[i]` = 以 i−1 结尾的连续 1，`right[i]` = 从 i+1 开始的连续 1 | 直观「删 i 后左右拼接」，O(n) 空间 |

面试里先写滑窗（通用），再提 `prev/cur` 作为 K=1 的 O(1) 简化。
"""
from typing import List


##################################################################################################
##### ! Solution 1: 滑动窗口，窗口内最多 1 个 0，答案 = 最大窗口长 − 1
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：面试标准答案；LC-1004 模板 K=1；−1 自动覆盖「必须删一个」
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def longestSubarray(self, nums: List[int]) -> int:
        l = zeros = best = 0
        for r, x in enumerate(nums):
            zeros += x == 0
            while zeros > 1:                            # ! 窗口里超过 1 个 0 → 收缩
                zeros -= nums[l] == 0; l += 1
            best = max(best, r - l + 1)
        return best - 1                                 # ! 删掉窗口里的一个元素


##################################################################################################
##### ! Solution 2: 两段连续 1 的长度 prev / cur（K = 1 专属的 O(1) 写法）
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：遇到 0 时「上一段 = 当前段，当前段清零」；答案 = max(prev + cur)；全 1 时同样要 −1
##################################################################################################


class Solution_2:
    def longestSubarray(self, nums: List[int]) -> int:
        prev = cur = best = 0                           # ! prev：上一个 0 之前那段连续 1 的长度
        for x in nums:
            if x:
                cur += 1
            else:
                prev, cur = cur, 0                      # ! 碰到 0：当前段变成「上一段」
            best = max(best, prev + cur)
        return best if best < len(nums) else best - 1   # ! 全是 1：没有 0 可删，只能删一个 1


##################################################################################################
##### ! Solution 3: 左右前缀数组 —— 删 i 后左右两段拼接
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：最直观的「枚举删哪个」：left[i] = 以 i-1 结尾的连续 1 长度，right[i] = 从 i+1 开始的；
#####         答案 = max(left[i] + right[i])。它也是最好的真值基线
##################################################################################################


class Solution_3:
    def longestSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        left, right = [0] * n, [0] * n
        for i in range(1, n):
            left[i] = left[i - 1] + 1 if nums[i - 1] else 0
        for i in range(n - 2, -1, -1):
            right[i] = right[i + 1] + 1 if nums[i + 1] else 0
        return max(left[i] + right[i] for i in range(n))


if __name__ == "__main__":
    import random
    cases = [([1, 1, 0, 1], 3), ([0, 1, 1, 1, 0, 1, 1, 0, 1], 5), ([1, 1, 1], 2), ([0], 0), ([0, 0], 0), ([1], 0), ([1, 0], 1)]
    for nums, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().longestSubarray(nums)
            assert got == want, (cls.__name__, nums, got, want)
    rng = random.Random(1493)
    for _ in range(5000):
        nums = [rng.randint(0, 1) for _ in range(rng.randint(1, 15))]
        outs = [cls().longestSubarray(nums) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (nums, outs)
    print("所有测试通过 ✓")
