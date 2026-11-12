from typing import List

from math import inf


class Solution_1_Trie_DP:
    def minValidStrings(self, words: List[str], target: str) -> int:
        trie = {}
        for w in words:
            node = trie
            for ch in w:
                node = node.setdefault(ch, {})

        n = len(target)
        dp = [inf] * (n + 1)        # dp[i]: target[i:] 最少切几段
        dp[n] = 0                   # 空串不用切
        for i in range(n - 1, -1, -1):
            node = trie
            for j in range(i, n):   # 枚举第一段 target[i..j],沿 Trie 边走边验证
                if target[j] not in node:
                    break           # 不是任何 word 的前缀,更长的也不可能是
                node = node[target[j]]
                dp[i] = min(dp[i], 1 + dp[j + 1])
        return dp[0] if dp[0] < inf else -1


"""
Preferred solution
"""
class Solution_2_Trie_Greedy:
    def minValidStrings(self, words: List[str], target: str) -> int:
        trie = {}
        for w in words:
            node = trie
            for ch in w:
                node = node.setdefault(ch, {})

        n = len(target)
        max_len = [0] * n           # max_len[i]: 从 i 出发最长能切多长(= 最多能往前跳几格)
        for i in range(n):
            node, j = trie, i
            while j < n and target[j] in node:
                node = node[target[j]]
                j += 1
            max_len[i] = j - i

        jumps = curr_end = curr_far = 0   # 已用段数、当前轮右端 R_k、下一轮右端 R_{k+1}
        for i in range(n):
            curr_far = max(curr_far, i + max_len[i])
            if i == curr_end:            # 当前轮扫完
                if curr_far == i:        # 一格都推不动,永远到不了
                    return -1
                jumps += 1
                curr_end = curr_far
                if curr_end >= n:        # 位置 n = 整个 target 拼完
                    return jumps
        return jumps
