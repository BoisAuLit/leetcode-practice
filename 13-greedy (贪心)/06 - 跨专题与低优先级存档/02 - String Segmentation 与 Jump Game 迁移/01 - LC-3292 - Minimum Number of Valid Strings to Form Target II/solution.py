from typing import List


class Solution:
    def minValidStrings(self, words: List[str], target: str) -> int:
        n = len(target)

        def z_function(s: str) -> List[int]:
            # z[i] = s 和 s[i:] 的最长公共前缀长度
            m = len(s)
            z = [0] * m
            l = r = 0  # 当前已知的最右匹配区间 [l, r)
            for i in range(1, m):
                if i < r:  # i 在已知区间内,先借用镜像位置的结果
                    z[i] = min(r - i, z[i - l])
                while i + z[i] < m and s[z[i]] == s[i + z[i]]:
                    z[i] += 1  # 从借来的长度继续往外暴力扩
                if i + z[i] > r:  # 更新最右区间
                    l, r = i, i + z[i]
            return z

        # max_len[p]: 从 target[p] 出发,最长能匹配到某个 word 前缀的长度
        max_len = [0] * n
        for w in words:
            z = z_function(w + "#" + target)
            off = len(w) + 1  # target 在拼接串里的起始下标
            for p in range(n):
                if z[off + p] > max_len[p]:
                    max_len[p] = z[off + p]

        # 45 题贪心,终点是 n,加上 -1 检测
        jumps = cur_end = cur_far = 0
        for i in range(n):
            cur_far = max(cur_far, i + max_len[i])
            if i == cur_end:
                if cur_far == i:
                    return -1
                jumps += 1
                cur_end = cur_far
                if cur_end >= n:
                    return jumps
        return jumps
