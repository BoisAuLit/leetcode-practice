"""LC-2958 - Length of Longest Subarray With at Most K Frequency

Level 1 · 02 变长窗口之最长合法区间 → Level 2 · 01 无重复与 Distinct 限制

题目在问：最长子数组，使其中**每个值的出现次数都 ≤ k**。

### LC-0003 的推广：k = 1 时就是「无重复字符的最长子串」

LC-0003 的窗口不变量：每个字符出现 ≤ 1 次。本题把 1 换成 k —— 代码上**只改一个比较**：

    cnt[x] += 1
    while cnt[x] > k:           # ! 0003 这里是 > 1；新进来的 x 是唯一可能超标的
        cnt[nums[l]] -= 1; l += 1

关键观察：**只有刚进窗口的 `nums[r]` 可能超过 k**（其他元素的计数没变），所以 while 条件只需检查 `cnt[nums[r]]`，不需要扫全表。
这是「最长合法窗口」模板的标准形态：右指针每进一个，左指针收缩到合法为止，窗口长度在每一步都取 max。

### 为什么不能用「atMost 计数」那套

那套是**数子数组个数**（LC-0992 / LC-1248），本题是**求最长**。两类模板的区别：
- 最长：每步 `best = max(best, r − l + 1)`
- 计数：每步 `res += r − l + 1`
"""
from collections import defaultdict
from typing import List


##################################################################################################
##### ! Solution 1: 滑动窗口 + 计数表，只检查刚进来的元素
##### ! 时间复杂度: O(n)   空间复杂度: O(不同值的个数)
##### ! 适用：面试标准答案；LC-0003 模板把「> 1」改成「> k」
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maxSubarrayLength(self, nums: List[int], k: int) -> int:
        cnt = defaultdict(int)
        l = best = 0
        for r, x in enumerate(nums):
            cnt[x] += 1
            while cnt[x] > k:                           # ! 只有 x 可能超标
                cnt[nums[l]] -= 1; l += 1
            best = max(best, r - l + 1)
        return best


##################################################################################################
##### ! Solution 2: 记录每个值出现位置的列表，超标时左指针直接跳到「第 (cnt−k) 次出现」之后
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：展示「左指针跳跃」的写法（LC-0003 的 last_seen 推广）：x 第 c 次出现在 r，
#####         若 c > k，左端至少要在 x 的第 (c−k) 次出现位置 + 1。l 只增不减，取 max
##################################################################################################


class Solution_2:
    def maxSubarrayLength(self, nums: List[int], k: int) -> int:
        pos = defaultdict(list)                         # ! pos[x] = x 出现过的所有下标
        l = best = 0
        for r, x in enumerate(nums):
            pos[x].append(r)
            if len(pos[x]) > k:
                l = max(l, pos[x][len(pos[x]) - k - 1] + 1)   # ! 跳过第 (c−k) 次出现
            best = max(best, r - l + 1)
        return best


##################################################################################################
##### ! Solution 3: 暴力 O(n²)（真值基线）
##### ! 时间复杂度: O(n²)   空间复杂度: O(n)
##### ! 适用：只用来对拍。固定左端向右扩，计数一旦超 k 就停
##################################################################################################


class Solution_3:
    def maxSubarrayLength(self, nums: List[int], k: int) -> int:
        n, best = len(nums), 0
        for i in range(n):
            cnt = defaultdict(int)
            for j in range(i, n):
                cnt[nums[j]] += 1
                if cnt[nums[j]] > k:
                    break
                best = max(best, j - i + 1)
        return best


if __name__ == "__main__":
    import random
    cases = [([1, 2, 3, 1, 2, 3, 1, 2], 2, 6), ([1, 2, 1, 2, 1, 2, 1, 2], 1, 2), ([5, 5, 5, 5, 5, 5, 5], 4, 4), ([1], 1, 1)]
    for nums, k, want in cases:
        for cls in (Solution_1, Solution_2, Solution_3):
            got = cls().maxSubarrayLength(nums, k)
            assert got == want, (cls.__name__, nums, k, got, want)
    rng = random.Random(2958)
    for _ in range(4000):
        nums = [rng.randint(1, 4) for _ in range(rng.randint(1, 14))]
        k = rng.randint(1, 4)
        outs = [cls().maxSubarrayLength(nums, k) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (nums, k, outs)
    print("所有测试通过 ✓")
