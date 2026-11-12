"""LC-1673 - Find the Most Competitive Subsequence

Level 1 · 03 单调栈与贪心构造 —— Greedy Monotonic Stack 的「保留 k 个」版本（第二轮自主新增）
题目在问：从 nums 里选出长度恰好为 k 的子序列，使它字典序最小（题目叫 most competitive）。

为什么新增它（和 LC-0402 / LC-0316 的区别，这是它的全部价值）：
        LC-0402：**删掉恰好 k 个** → 预算写成「还能删几个」
        LC-1673：**保留恰好 k 个** → 预算写成「后面还够不够补满」
        LC-0316：**每种字符恰好一次** → 预算写成「这个字符后面还会不会再出现」
  三题共用同一个贪心单调栈骨架，差别只在「什么时候允许 Pop」这一个判断。
  把三者放在一起，就能把「安全删除的条件」这件事彻底想清楚，而不是背三份代码。

决定性观察：
  1. 字典序比较是**从左往右逐位**的，所以越靠前的位置越值钱：
     只要能让前面的某一位变小，哪怕后面全变大也是赚的。
  2. 因此当 `stack[-1] > nums[i]` 时，想把栈顶换成更小的 nums[i]。
  3. 但不能无条件换 —— 必须保证**最后还能凑够 k 个**。
     剩余可用元素个数 = n - i（含当前这个），已选 len(stack) 个。
     弹掉栈顶后还剩 len(stack)-1 个，必须满足 `len(stack) - 1 + (n - i) >= k`。
     整理一下就是常用的写法：`len(stack) + (n - i) > k`。

Pop 条件（完整）：
        stack and stack[-1] > nums[i] and len(stack) + (n - i) > k
  三个条件缺一不可：
    - `stack[-1] > nums[i]`：严格大于才换。相等时换没有收益，还白白消耗了「后面元素」的额度。
    - 长度检查：这就是本题独有的、替代 LC-0402 中 k 计数器的「安全删除」条件。

Push 之后还要截断：栈可能超过 k（后面的元素一直在变大、弹不动时）。
      所以 `if len(stack) < k: stack.append(x)`，或者最后 `return stack[:k]`。本文件用前者。

为什么贪心是对的（简短证明）：
  设最优解在第 p 位放了 v，而我们的算法在第 p 位放了 u < v。
  算法能放下 u，说明 u 的位置之后仍有足够元素补满剩下的位数，
  于是「前 p-1 位相同、第 p 位用 u」构成一个合法子序列，它字典序严格小于最优解 —— 矛盾。

复杂度：O(n) 时间（每个元素最多入栈出栈各一次），O(k) 空间。

边界：
  - k == len(nums) → 原数组照抄（一个都不能删）
  - 全递增 [1,2,3,4], k=2 → [1,2]（栈永远弹不动，靠长度截断）
  - 全递减 [4,3,2,1], k=2 → [2,1]（一路弹到底）
  - 有重复 [2,2,2], k=2 → [2,2]（相等不弹）
"""

from typing import List


##################################################################################################
##### ! Solution 1: 贪心单调栈 + 「剩余元素够不够补满 k」的安全删除条件
##### ! 时间复杂度: O(n)   空间复杂度: O(k)
##### ! 适用：所有「选恰好 k 个使字典序最优」的题；和 LC-0402 互为镜像
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def mostCompetitive(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        stack: List[int] = []
        for i, x in enumerate(nums):
            # ! 严格大于才换；且弹掉之后后面还必须够补满 k 个
            while stack and stack[-1] > x and len(stack) + (n - i) > k:
                stack.pop()
            if len(stack) < k:           # ! 已经选够 k 个就不再 push（否则要末尾截断）
                stack.append(x)
        return stack


##################################################################################################
##### ! Solution 2: 换算成「删掉 n-k 个」，完全复用 LC-0402 的删除预算模板
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：用来看清 1673 和 0402 其实是同一道题的两种说法
##################################################################################################


class Solution_2:
    def mostCompetitive(self, nums: List[int], k: int) -> List[int]:
        remove = len(nums) - k           # ! 「保留 k 个」==「删掉 n-k 个」
        stack: List[int] = []
        for x in nums:
            while stack and remove > 0 and stack[-1] > x:
                stack.pop()
                remove -= 1
            stack.append(x)
        while remove > 0:                # ! 预算没花完就从末尾删（末尾是最不值钱的位）
            stack.pop()
            remove -= 1
        return stack


##################################################################################################
##### ! Solution 3: 逐位贪心 —— 每一位在允许范围内找最小值（基准答案，用来对拍）
##### ! 时间复杂度: O(n * k) 最坏 O(n^2)   空间复杂度: O(k)
##### ! 适用：正确性参照；也是最容易口头解释清楚的版本
##################################################################################################


class Solution_3:
    def mostCompetitive(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        res: List[int] = []
        start = 0
        for pos in range(k):
            # ! 第 pos 位只能从 [start, n-(k-pos)] 里选，否则后面补不满
            limit = n - (k - pos)
            best = start
            for j in range(start, limit + 1):
                if nums[j] < nums[best]:
                    best = j
            res.append(nums[best])
            start = best + 1
        return res


if __name__ == "__main__":
    import random

    cases = [([3, 5, 2, 6], 2), ([2, 4, 3, 3, 5, 4, 9, 6], 4), ([1, 2, 3, 4], 2),
             ([4, 3, 2, 1], 2), ([2, 2, 2], 2), ([5], 1), ([3, 1, 2], 3)]
    for nums, k in cases:
        a = Solution_1().mostCompetitive(nums, k)
        assert a == Solution_2().mostCompetitive(nums, k) == Solution_3().mostCompetitive(nums, k), (nums, k)
        print(f"{nums}, k={k} -> {a}")

    for _ in range(500):                 # ! 随机对拍，含大量重复值
        nums = [random.randint(1, 4) for _ in range(random.randint(1, 10))]
        k = random.randint(1, len(nums))
        assert (Solution_1().mostCompetitive(nums, k)
                == Solution_2().mostCompetitive(nums, k)
                == Solution_3().mostCompetitive(nums, k)), (nums, k)
    print("随机对拍 500 组通过 ✓")
