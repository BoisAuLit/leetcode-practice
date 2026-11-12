# https://leetcode.com/problems/minimum-number-of-valid-strings-to-form-target-i/

from typing import List


class Solution:
    def minValidStrings(self, words: List[str], target: str) -> int:
        n = len(target)
        trie = {}
        # ! 字典树必然建立在一系列 words 之上, 必须要有好几个 words 才可以的
        for word in words:
            node = trie
            for ch in word:
                node = node.setdefault(ch, {})
            # ! 第一, 下面这一行纯属浪费, 无用
            node["#"] = word
        max_steps = [0] * n
        for i in range(n):
            level = 0
            node = trie
            for j in range(i, n):
                ch = target[j]
                if ch not in node:
                    break
                node = node[ch]
                level += 1
            max_steps[i] = level

        curr_far = curr_end = 0
        steps = 0
        for i in range(n):
            curr_far = max(curr_far, i + max_steps[i])
            if i == curr_end:
                curr_end = curr_far
                steps += 1
                if curr_end >= n:  # 更新之后再判是否够到终点
                    return steps

        """
        能走到这一行,说明循环里从来没有 return 过, 也就是 << 中途卡住了 >>
        也就是说, 在某个 i == curr_end 的时刻, curr_far 没有推进,
        curr_end 从此定在那里,后面所有的 i 都比它大,再也不会更新。


        但 curr_far 不一样——curr_far = max(curr_far, i + max_steps[i]) 这一行每个 i 都会执行,不管 i 到底能不能到达。卡住之后,循环继续往右扫,那些根本到不了的位置照样把它们的 i + max_steps[i] 混进了 curr_far。于是出现这种情况:明明从起点走不通,curr_far 却被某个"到不了的位置"推到了 n。
        """
        return steps if curr_end == n else -1


##################################################################################################
##### ! Solution DP: 来自 12-dynamic-programming 的另一份实现（同一道题的 DP 视角）
##### ! 这道题在仓库里曾有三份实体目录（本专题 / 12-DP / 13-greedy 的 Jump Game II - Cluster）。
#####   本次统一成**一份**：本目录是正式位置（它有 note.md、讲解图，以及 4 条复习记录），
#####   12-DP 的那份已改为索引 README，13-greedy 的那份已归档为「变体 · …」不参与复习队列。
##### ! 下面把 12-DP 版的实现原样搬过来（类名加 _DP 后缀），方便对照两种写法。
##################################################################################################


from math import inf


from typing import List


class Solution_DP:
    def minValidStrings(self, words: List[str], target: str) -> int:
        trie = {}
        for word in words:
            node = trie
            for ch in word:
                node = node.setdefault(ch, {})
            node["#"] = word
        n = len(target)
        dp = [inf] * (n + 1)
        dp[n] = 0
        for i in range(n - 1, -1, -1):
            node = trie
            for j in range(i, n):
                if target[j] in node:
                    node = node[target[j]]
                else:
                    break
                dp[i] = min(dp[i], 1 + dp[j + 1])
        return dp[0] if dp[0] < inf else -1
