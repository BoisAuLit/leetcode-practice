"""LC-0491 - Non-decreasing Subsequences（第二轮自主新增）

Level 1 · 01 子集、组合与目标和 —— **不能排序时怎么去重**
题目在问：返回所有长度 >= 2 的**非递减**子序列，**结果不能重复**。

为什么新增它（它补的是哪个缺口 —— 这是本题的全部价值）：
  LC-0090 Subsets II 和 LC-0040 Combination Sum II 的去重套路都是：
      **先排序**，然后 `if i > start and nums[i] == nums[i-1]: continue`
      （同一层里跳过相邻的重复值）。
  **但这道题不能排序** —— 排序会破坏「子序列」的原始顺序，答案就全错了。

  于是必须换一种去重方式：**在每一层用一个局部 set 记录「本层已经用过哪些值」**。
  这是一个独立、且非常常用的技巧，本专题原本完全没有练到。

两种去重方式的对照（本章最该记住的一张表）：

| | 排序 + 相邻跳过（LC-0090 / LC-0040） | **每层 set**（本题） |
|---|---|---|
| 前提 | **允许排序** | 顺序不能动 |
| 写法 | `if i > start and nums[i]==nums[i-1]: continue` | `if nums[i] in used_this_level: continue` |
| 额外空间 | O(1) | O(本层宽度) |
| 为什么对 | 排序后相同的值一定相邻，同层只取第一个 | 同层同值的分支完全同构，只保留一个 |

**两者的共同本质**：
> **去重去的是「同一层里的重复选择」，不是「同一条路径上的重复元素」。**
> 同一条路径上出现相同的值是**合法的**（`[1,1]` 本身就是一个合法答案）。

决定性观察：
  1. 回溯状态：`dfs(start, path)`，从 `start` 开始挑下一个元素。
  2. **两个约束**：
     - 非递减：`nums[i] >= path[-1]`（path 非空时）
     - 去重：`nums[i]` 在**本层**没用过
  3. **收集时机**：`len(path) >= 2` 就记一个答案，但**不要 return** ——
     还要继续往后接更长的。这和「只在叶子收集」的题不同。

复杂度：最坏 **O(2^n · n)**（答案本身就可能有 2^n 个，每个长度 O(n)）。
      空间 O(n) 递归栈 + O(答案总长度)。
      **这类「返回所有方案」的题，复杂度下界就是答案的规模**，没法更快。

边界：
  - `[4,6,7,7]` → `[[4,6],[4,6,7],[4,6,7,7],[4,7],[4,7,7],[6,7],[6,7,7],[7,7]]`
  - `[4,4,3,2,1]` → `[[4,4]]`
  - 全部相同 `[2,2,2]` → `[[2,2],[2,2,2]]`
  - 含负数（题目范围 -100..100）
  - 长度 < 2 → `[]`
"""

from typing import List


##################################################################################################
##### ! Solution 1: 回溯 + **每层 set 去重**（不能排序时的标准做法）
##### ! 时间复杂度: O(2^n · n)   空间复杂度: O(n) 递归栈
##### ! 适用：顺序不能改、又要去重的子序列枚举；和「排序+相邻跳过」互为补充
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findSubsequences(self, nums: List[int]) -> List[List[int]]:
        res: List[List[int]] = []
        path: List[int] = []

        def dfs(start: int) -> None:
            if len(path) >= 2:
                res.append(path[:])          # ! 收集后**不要 return**，还能继续接长
            used = set()                     # ! 只在「本层」有效：同一层同一个值只选一次
            for i in range(start, len(nums)):
                if path and nums[i] < path[-1]:
                    continue                 # ! 破坏非递减
                if nums[i] in used:
                    continue                 # ! 本层已经用过这个值，分支同构，跳过
                used.add(nums[i])
                path.append(nums[i])
                dfs(i + 1)
                path.pop()                   # ! 回溯

        dfs(0)
        return res


##################################################################################################
##### ! Solution 2: 枚举所有 2^n 个子序列，用 set 去重（基准答案，用来对拍）
##### ! 时间复杂度: O(2^n · n)   空间复杂度: O(2^n · n)
##### ! 适用：正确性参照 —— 直接按定义枚举，不依赖任何去重技巧
##################################################################################################


class Solution_2:
    def findSubsequences(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        seen = set()
        for mask in range(1 << n):
            sub = [nums[i] for i in range(n) if mask >> i & 1]
            if len(sub) >= 2 and all(sub[i] <= sub[i + 1] for i in range(len(sub) - 1)):
                seen.add(tuple(sub))
        return [list(t) for t in seen]


if __name__ == "__main__":
    import random

    cases = [[4, 6, 7, 7], [4, 4, 3, 2, 1], [2, 2, 2], [1], [], [1, 2, 3, 4],
             [-1, -1, 0], [3, 1, 2, 2]]
    for nums in cases:
        a = sorted(Solution_1().findSubsequences(nums))
        b = sorted(Solution_2().findSubsequences(nums))
        assert a == b, (nums, a, b)
        print(f"{nums} -> {len(a)} 个: {a[:4]}{' ...' if len(a) > 4 else ''}")

    for _ in range(1000):                # ! 小值域随机对拍，专压重复元素
        nums = [random.randint(0, 3) for _ in range(random.randint(0, 9))]
        a = sorted(Solution_1().findSubsequences(nums))
        b = sorted(Solution_2().findSubsequences(nums))
        assert a == b, (nums, a, b)
    print("随机对拍 1000 组通过 ✓（每层 set 去重 == 全枚举后去重）")
