"""LC-0421 - Maximum XOR of Two Numbers in an Array

Level 1 · 05 进阶变体 —— **Bitwise Trie（二进制字典树）**
题目在问：数组里任选两个数，求 `a XOR b` 的最大值。

核心转换：**把整数看成一个固定长度的「0/1 字符串」，Trie 的边从 26 个字母变成 2 个 bit。**

先复习 XOR：
  `0^0=0, 1^1=0, 0^1=1, 1^0=1` —— **两位不同才得 1**。
  所以要让 XOR 大，就要让**高位尽量不同**。

决定性观察：
  1. **必须从最高位开始**。因为高位的 1 比后面所有位加起来都值钱
     （`2^k > 2^(k-1) + ... + 2^0`），所以贪心地优先让高位取 1 永远不亏。
     这是本题贪心成立的全部理由。
  2. 把每个数按**从高到低**的固定位宽（题目 `nums[i] <= 2^31-1`，取 32 位或 31 位）
     插进一棵只有两个 children（`0` / `1`）的 Trie。
  3. 查询 x 的最大搭档：在每一位上**优先走与 x 当前位相反的分支**
     （相反 ⟹ 这一位 XOR 出 1）；那条分支不存在就只能走相同的。
  4. 对每个数都查一次，取最大值。

**为什么 TrieNode 只有两个 children**：二进制只有 0 和 1 两种边。
     这让 Bitwise Trie 比字符 Trie 简单得多，但思想完全一致。

复杂度：**O(n · B)**，B 是位宽（这里 32）。
     也就是 O(32n) ≈ O(n)，空间 O(n · B)。
     对比暴力两两异或的 O(n²)：n = 2×10⁵ 时暴力 4×10¹⁰ 必然超时。

还有一种**不用 Trie** 的经典解法（前缀 + Hash Set，见 Solution_2）：
     从高位往低位逐位确定答案，每一位先假设能填 1，
     用 `a ^ b = target ⟺ a ^ target = b` 在 set 里验证。同样 O(32n)。
     面试里两种都值得会 —— Trie 版更直观，Hash Set 版代码更短。

标记 **P2**：它是 Bit Manipulation + Trie 的组合，
     不必作为 FAANG 准备的核心必背模板，但值得理解「Trie 的边不一定是字母」。

边界：
  - 只有两个数
  - 含 0
  - 所有数相同 → 答案 0
  - 数组长度 < 2（题目保证 >= 1，但这里也处理了）
"""

from typing import List

BITS = 31          # ! nums[i] <= 2^31 - 1，31 位足够


class BitTrieNode:
    __slots__ = ("children",)

    def __init__(self):
        self.children = [None, None]     # ! 只有两条边：bit 0 和 bit 1


##################################################################################################
##### ! Solution 1: Bitwise Trie —— 从高位插入，查询时优先走相反 bit
##### ! 时间复杂度: O(n · 31)   空间复杂度: O(n · 31)
##### ! 适用：所有「最大/最小 XOR 配对」问题；LC-1707 是它的带约束版本
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def findMaximumXOR(self, nums: List[int]) -> int:
        root = BitTrieNode()
        for x in nums:                               # ! 插入：从最高位到最低位
            node = root
            for b in range(BITS, -1, -1):
                bit = (x >> b) & 1
                if node.children[bit] is None:
                    node.children[bit] = BitTrieNode()
                node = node.children[bit]

        best = 0
        for x in nums:                               # ! 查询：每一位都想要「不同」
            node, cur = root, 0
            for b in range(BITS, -1, -1):
                bit = (x >> b) & 1
                want = 1 - bit                       # ! 相反的 bit 才能让这一位 XOR 出 1
                if node.children[want] is not None:
                    cur |= (1 << b)                  # ! 这一位拿到 1
                    node = node.children[want]
                else:
                    node = node.children[bit]        # ! 只能走相同的，这一位是 0
            best = max(best, cur)
        return best


##################################################################################################
##### ! Solution 2: 逐位贪心 + Hash Set（不用 Trie，代码更短）
##### ! 时间复杂度: O(n · 31)   空间复杂度: O(n)
##### ! 适用：面试里想快速写完时；原理是 a ^ b = target ⟺ a ^ target = b
##################################################################################################


class Solution_2:
    def findMaximumXOR(self, nums: List[int]) -> int:
        best = 0
        for b in range(BITS, -1, -1):
            best <<= 1
            candidate = best | 1                     # ! 假设这一位也能取到 1
            prefixes = {x >> b for x in nums}        # ! 只看每个数的高位前缀
            # ! 若存在 p1 ^ p2 == candidate，则 candidate 可达
            if any(candidate ^ p in prefixes for p in prefixes):
                best = candidate
        return best


##################################################################################################
##### ! Solution 3: 暴力两两异或（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(1)
##### ! 适用：正确性参照；n 大时必然超时
##################################################################################################


class Solution_3:
    def findMaximumXOR(self, nums: List[int]) -> int:
        best = 0
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                best = max(best, nums[i] ^ nums[j])
        return best


if __name__ == "__main__":
    import random

    cases = [[3, 10, 5, 25, 2, 8], [0], [2, 4], [8, 10, 2], [14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70],
             [5, 5, 5], [0, 0]]
    for nums in cases:
        a = Solution_1().findMaximumXOR(nums)
        b = Solution_2().findMaximumXOR(nums)
        c = Solution_3().findMaximumXOR(nums)
        assert a == b == c, (nums, a, b, c)
        print(f"{nums} -> {a}")

    for _ in range(500):
        nums = [random.randint(0, 1 << 20) for _ in range(random.randint(1, 12))]
        a = Solution_1().findMaximumXOR(nums)
        b = Solution_2().findMaximumXOR(nums)
        c = Solution_3().findMaximumXOR(nums)
        assert a == b == c, (nums, a, b, c)
    print("随机对拍 500 组通过 ✓（Bitwise Trie == 逐位贪心 == 暴力）")
