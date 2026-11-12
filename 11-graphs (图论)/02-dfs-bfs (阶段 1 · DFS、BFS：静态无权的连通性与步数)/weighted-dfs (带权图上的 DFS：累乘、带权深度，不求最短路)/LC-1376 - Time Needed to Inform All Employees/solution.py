"""LC-1376 - Time Needed to Inform All Employees

阶段 1 · 带权图上的 DFS（带权深度，不求最短路） ○ 核心变体
题目在问：消息从 CEO 一层层往下传，每个经理通知完直属下属要 informTime[i] 分钟，全员收到要多久
点是什么：一个员工   边是什么：经理 -> 直属下属，边权 = 经理的 informTime（一棵树，manager[] 是父指针）
和签名题比改了哪一行：200 的 DFS 只问"能不能到"，这里 DFS 要带着"到这里花了多久"往下走，
    答案 = 根到叶子的最大带权深度。注意 manager[] 给的是父指针，要先反过来建 children 表才能从 CEO 往下走
"""
import sys
from collections import deque
from typing import List

sys.setrecursionlimit(10**6)  # ! 公司可能是一条 1e5 长的链，递归版 DFS 要放开深度限制

##################################################################################################
##### ! Solution 1: 自顶向下递归 DFS（返回"子树通知完"的用时）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)   children 表 + 递归栈
##### ! 适用：树上"带权深度最大值"的标准写法；手册点名的解法
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def numOfMinutes(self, n: int, headID: int, manager: List[int], informTime: List[int]) -> int:
        children = [[] for _ in range(n)]
        for i, m in enumerate(manager):  # ! 父指针反过来，才能从 CEO 往下走
            if m != -1:
                children[m].append(i)

        def dfs(u: int) -> int:
            # ! 返回：u 收到消息后，u 的整棵子树全部收到还要多久
            slowest = 0
            for v in children[u]:
                slowest = max(slowest, dfs(v))  # ! 下属是同时被通知的，只看最慢那一支
            return informTime[u] + slowest  # ! 叶子 informTime 为 0，自然返回 0

        return dfs(headID)


##################################################################################################
##### ! Solution 2: BFS 带着累计时间往下传
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：不想碰递归深度时用；队列里存 (员工, 收到消息的时刻)，答案 = 出现过的最大时刻
##################################################################################################


class Solution_2:
    def numOfMinutes(self, n: int, headID: int, manager: List[int], informTime: List[int]) -> int:
        children = [[] for _ in range(n)]
        for i, m in enumerate(manager):
            if m != -1:
                children[m].append(i)

        ans = 0
        queue = deque([(headID, 0)])  # ! (员工, 他收到消息的时刻)
        while queue:
            u, t = queue.popleft()
            ans = max(ans, t)
            for v in children[u]:
                queue.append((v, t + informTime[u]))  # ! 下属在 u 通知完之后才收到
        return ans


##################################################################################################
##### ! Solution 3: 自底向上沿 manager[] 往上爬 + 记忆化
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：不建 children 表，直接用父指针；每个员工往上爬到第一个已算出的祖先，再把沿途回填
##################################################################################################


class Solution_3:
    def numOfMinutes(self, n: int, headID: int, manager: List[int], informTime: List[int]) -> int:
        time_to = [-1] * n  # ! time_to[i] = 消息传到 i 的时刻；-1 = 还没算
        time_to[headID] = 0
        ans = 0
        for i in range(n):
            path = []
            u = i
            while time_to[u] == -1:  # ! 往上爬，直到碰见算过的祖先（最多爬到 CEO）
                path.append(u)
                u = manager[u]
            t = time_to[u]
            for v in reversed(path):  # ! 从祖先往下回填：到 v 的时刻 = 到上级的时刻 + 上级的 informTime
                t += informTime[manager[v]]
                time_to[v] = t
            ans = max(ans, time_to[i])
        return ans  # ! 每个员工只会被回填一次，整体 O(n)


s = Solution_1()
n = 1
headID = 0
manager = [-1]
informTime = [0]
result = s.numOfMinutes(n, headID, manager, informTime)
print(result)  # 0

n = 6
headID = 2
manager = [2, 2, -1, 2, 2, 2]
informTime = [0, 0, 1, 0, 0, 0]
result = s.numOfMinutes(n, headID, manager, informTime)
print(result)  # 1
