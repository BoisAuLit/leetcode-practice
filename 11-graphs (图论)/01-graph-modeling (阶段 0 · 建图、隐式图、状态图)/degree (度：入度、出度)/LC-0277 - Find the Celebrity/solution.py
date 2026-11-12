"""LC-0277 - Find the Celebrity

阶段 0 · 建图、隐式图、状态图 · 度(入度、出度) ○ 核心(premium，手册题单外的 997 同款)
题目在问：n 个人，只能通过 knows(a, b) 问 "a 认识 b 吗"，找那个所有人都认识他、他谁也不认识的名人；没有就 -1
点是什么：人(0..n-1)   边是什么：a 认识 b 的有向边，但边不给你，只能一条一条问 knows
和签名题比改了哪一行：和 997 一样是 "入度 n-1、出度 0"，区别是边表藏在 API 里，问一次算一次，
  所以不能 O(n²) 把图问全，要用一条边同时淘汰一个人：knows(c, i) 为真则 c 出局、否则 i 出局
"""
from functools import lru_cache


def knows(a: int, b: int):
    pass


##################################################################################################
##### ! Solution 1: 两趟淘汰(用户原版，class 名为 Solution)
##### ! 时间复杂度: O(n) 次 knows 调用   空间复杂度: O(n)   lru_cache 存下问过的答案，验证趟不重复问
##### ! 适用：标准答案；第一趟 n-1 次问出唯一候选，第二趟最多 2(n-1) 次验证
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution:
    @lru_cache(maxsize=None)
    def cachedKnows(self, a, b):
        return knows(a, b)

    def findCelebrity(self, n: int) -> int:
        self.n = n
        celebrity_candidate = 0
        for i in range(1, n):
            if self.cachedKnows(celebrity_candidate, i):
                celebrity_candidate = i
        if self.is_celebrity(celebrity_candidate):
            return celebrity_candidate
        return -1

    def is_celebrity(self, i):
        for j in range(self.n):
            if i == j:
                continue
            if self.cachedKnows(i, j) or not self.cachedKnows(j, i):
                return False
        return True


##################################################################################################
##### ! Solution 2: 暴力数度(997 的写法照搬)
##### ! 时间复杂度: O(n²) 次 knows 调用   空间复杂度: O(n)   把隐藏的邻接矩阵整张问出来
##### ! 适用：只做 baseline 用，n 大了会超时；但它说明了本题和 997 是同一个 "度" 问题
##################################################################################################


class Solution_2:
    def findCelebrity(self, n: int) -> int:
        in_deg = [0] * n
        out_deg = [0] * n
        for a in range(n):
            for b in range(n):
                if a != b and knows(a, b):  # ! 每条可能的边都问一遍
                    out_deg[a] += 1
                    in_deg[b] += 1
        for i in range(n):
            if in_deg[i] == n - 1 and out_deg[i] == 0:
                return i
        return -1


##################################################################################################
##### ! Solution 3: 栈两两淘汰 + 验证
##### ! 时间复杂度: O(n) 次 knows 调用   空间复杂度: O(n)   栈里每弹两个人问一次，淘汰一个塞回一个
##### ! 适用：和 Solution 1 同一个思想的另一种画面：每次 knows(a, b) 必定淘汰 a、b 之一
##################################################################################################


class Solution_3:
    def findCelebrity(self, n: int) -> int:
        stack = list(range(n))
        while len(stack) > 1:
            a, b = stack.pop(), stack.pop()
            # ! a 认识 b → a 不是名人，b 留下；否则 b 没被 a 认识 → b 不是名人，a 留下
            stack.append(b if knows(a, b) else a)
        c = stack[0]
        for i in range(n):  # ! 验证：c 谁都不认识，且所有人都认识 c
            if i != c and (knows(c, i) or not knows(i, c)):
                return -1
        return c


# ! 本地 mock：LeetCode 平台提供 knows(a, b)，这里用一张关系矩阵顶替上面的占位 stub，让文件能直接跑
KNOWS = [
    [1, 1, 0],
    [0, 1, 0],
    [1, 1, 1],
]  # 示例 1：KNOWS[i][j] = 1 表示 i 认识 j，1 号谁都不认识、所有人都认识他 → 名人是 1


def knows(a: int, b: int) -> bool:
    return KNOWS[a][b] == 1


s = Solution()
n = 3
result = s.findCelebrity(n)
print(result)  # 1
