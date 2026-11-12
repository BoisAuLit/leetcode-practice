"""LC-0330 - Patching Array（第二轮自主新增）

Level 1 · 01 跳跃、可达性与区间覆盖 —— **「当前能覆盖到多远」的贪心**（Jump Game 的数论版）
题目在问：给一个升序数组 nums 和 n，最少添加几个数，
         才能让 `[1, n]` 里**每个整数**都能表示成某些元素之和？

为什么新增它（它补的是哪个缺口）：
  LC-0055 / LC-0045 / LC-1024 的「最远可达」都是**下标/区间**上的覆盖。
  这道题的「可达范围」是**数值的和**，而且有一个漂亮的倍增性质 ——
  同一个「维护 reach、不够就补」的骨架换了一个完全不同的舞台。
  这是本章最能说明「贪心的本质是维护一个可达边界」的一题。

决定性观察（核心不变量 + 为什么补 `reach` 最优）：
  1. 维护 **`reach`** = 「目前为止 `[1, reach]` 里的每个整数都能表示出来」。
     初始 `reach = 0`（什么都表示不出来）。
  2. 遍历 nums（升序）：
     - 若 `nums[i] <= reach + 1`：**它能接上** ⟹ 新的覆盖范围扩展到 `reach + nums[i]`。
       （因为 `[1, reach]` 都能表示，加上 `nums[i]` 就能表示
        `[nums[i], reach + nums[i]]`，两段**连起来了**，前提是 `nums[i] <= reach + 1`。）
     - 若 `nums[i] > reach + 1`：**有缺口** ⟹ `reach + 1` 表示不出来 ⟹ 必须补一个数。
  3. **补什么数最优？补 `reach + 1`。**
     - 必须能表示出 `reach + 1`，所以补的数 **不能超过** `reach + 1`。
     - 补 `x <= reach + 1` 之后，覆盖范围变成 `reach + x`，**x 越大越好**。
     - ⟹ 补 `reach + 1`，覆盖范围**直接翻倍变成 `2 * reach + 1`**。
     这就是为什么答案是 O(log n) 量级的。∎
  4. 循环直到 `reach >= n`。

```python
patches = i = 0
reach = 0
while reach < n:
    if i < len(nums) and nums[i] <= reach + 1:
        reach += nums[i]      # 能接上，扩展
        i += 1
    else:
        reach += reach + 1    # 补 reach+1，范围翻倍
        patches += 1
return patches
```

> **和 Jump Game 的对照**：
> | | LC-0055 / 0045 | LC-0330 本题 |
> |---|---|---|
> | reach 的含义 | 能走到的**最远下标** | 能表示出的**最大整数**（且 [1, reach] 全覆盖） |
> | 扩展方式 | `max(reach, i + nums[i])` | `reach += nums[i]` |
> | 不够时 | 返回 False / 再跳一次 | **补一个数，范围翻倍** |
>
> **三道题的骨架完全一样：维护可达边界，不够就付代价。**

复杂度：**O(m + log n)** 时间（m = len(nums)），O(1) 空间。
      补的次数是 O(log n)，因为每次补都让 reach 至少翻倍。

**溢出提醒**：`reach` 可能超过 32 位（n 可达 2³¹−1）。Python 无所谓，
但 C++/Java 要用 long。面试要提一句。

边界：
  - nums 为空 → 需要补 `log2(n)+1` 个（1, 2, 4, 8, ...）
  - nums 已经够了 → 0
  - `nums = [1,3], n = 6` → 1（补 2）
  - `nums = [1,5,10], n = 20` → 2（补 2 和 4）
  - `nums = [1,2,2], n = 5` → 0
  - `nums = [2], n = 3` → 1（补 1 之后 {1,2} 覆盖 1、2、3）
  - nums 里有超过 n 的元素（可以直接忽略）
"""

from typing import List


##################################################################################################
##### ! Solution 1: 维护 reach（[1, reach] 全可表示），不够就补 reach+1 让范围翻倍
##### ! 时间复杂度: O(m + log n)   空间复杂度: O(1)
##### ! 适用：「维护可达边界、不够就付代价」—— 和 Jump Game 系列同一个骨架
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def minPatches(self, nums: List[int], n: int) -> int:
        patches = 0
        i = 0
        reach = 0                  # ! 不变量：[1, reach] 里每个整数都能被表示出来
        while reach < n:
            if i < len(nums) and nums[i] <= reach + 1:
                reach += nums[i]   # ! 能接上（没有缺口），覆盖范围直接相加
                i += 1
            else:
                reach += reach + 1  # ! 补 reach+1 ⟹ 范围翻倍（这是最优的补法）
                patches += 1
        return patches


##################################################################################################
##### ! Solution 2: 暴力 —— 用可达集合逐个验证（基准答案，用来对拍；只适合很小的 n）
##### ! 时间复杂度: O(2^m + 补的次数 · n)   空间复杂度: O(n)
##### ! 适用：正确性参照 —— 直接按「每个 [1,n] 的数都能表示成子集和」的定义验证
##################################################################################################


class Solution_2:
    def minPatches(self, nums: List[int], n: int) -> int:
        def reachable(arr):
            """返回 [1, n] 里能被表示出来的集合（子集和）。"""
            poss = {0}
            for x in arr:
                poss |= {p + x for p in poss if p + x <= n}
            return poss

        cur = list(nums)
        patches = 0
        while True:
            poss = reachable(cur)
            missing = next((k for k in range(1, n + 1) if k not in poss), None)
            if missing is None:
                return patches
            cur.append(missing)      # ! 补上最小的那个缺口（可以证明这是最优的）
            patches += 1


if __name__ == "__main__":
    import random

    # ! [2], n=3 只需补 1 个（补 1 之后 {1,2} 能表示 1、2、3）
    cases = [([1, 3], 6, 1), ([1, 5, 10], 20, 2), ([1, 2, 2], 5, 0),
             ([], 7, 3), ([1], 1, 0), ([2], 3, 1), ([1, 2, 31, 33], 2147483647, 28)]
    for nums, n, want in cases:
        a = Solution_1().minPatches(nums[:], n)
        assert a == want, (nums, n, a, want)
        print(f"nums={nums}, n={n} -> {a}")

    for _ in range(400):                 # ! 小 n 随机对拍（暴力版只能跑小输入）
        n = random.randint(1, 25)
        m = random.randint(0, 4)
        nums = sorted(random.randint(1, 12) for _ in range(m))
        a = Solution_1().minPatches(nums[:], n)
        b = Solution_2().minPatches(nums[:], n)
        assert a == b, (nums, n, a, b)
    print("随机对拍 400 组通过 ✓（reach 翻倍贪心 == 逐个补最小缺口的暴力）")
