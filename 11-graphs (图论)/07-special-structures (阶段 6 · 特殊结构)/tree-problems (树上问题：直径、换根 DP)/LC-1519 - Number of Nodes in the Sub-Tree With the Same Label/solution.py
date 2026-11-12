"""LC-1519 - Number of Nodes in the Sub-Tree With the Same Label（第二轮自主新增）

阶段 6 · 树上问题 —— **自底向上合并子树的统计量（小技巧：合并计数表）**
题目在问：一棵以 0 为根的树，每个节点有一个小写字母标签。
         对每个节点 i，求「以 i 为根的子树里，和 i 标签相同的节点有几个」（含自己）。

点是什么：树节点。边是什么：给定的无向边（要自己定根、自己防止走回父亲）。

为什么新增它（它补的是哪个缺口）：
  本模板原有的题目是「直径」「换根 DP」。这道题练的是另一个高频技能：
  **把子树的统计量（这里是一张 26 维计数表）自底向上合并到父亲**。
  这是树上统计题最通用的骨架（子树大小、子树中某值的个数、子树颜色数…都靠它），
  而且它展示了一个重要的工程细节：**合并时要选大的那个当底、把小的并进去**，
  否则复杂度会退化。

决定性观察：
  1. **无根树要自己定根**（题目说以 0 为根），并且 DFS 时要**记住父亲**以免走回去
     —— 树的无向边列表没有方向，这一点必须手动处理。
  2. `dfs(u)` 返回「u 子树里每个字母的出现次数」（一个长度 26 的表）。
     答案 `ans[u] = 子树计数表[labels[u]]`。
  3. **合并的细节**：把所有孩子的表加到自己的表上。
     - 朴素做法：每个节点新建一个长度 26 的表，合并是 O(26)
       ⟹ 总共 **O(26 · n)**，对 n ≤ 10⁵ 完全够用。这是本题的标准解。
     - 如果标签不是只有 26 种而是任意值，就要用 dict 并采用
       **小表合并进大表（small-to-large / DSU on tree）**，否则会退化。
       本文件的 Solution_2 演示了这个通用技巧。
  4. **必须用迭代 DFS 或提高递归上限**：n 可达 10⁵，链状树会把 Python 默认递归深度撑爆。
     本文件 Solution_1 用**显式栈的迭代后序**，从根本上避免这个问题。

复杂度：**O(26 · n)** 时间（Solution_1），O(26 · n) 空间。
      Solution_2 的小表合并是 O(n log n) 量级（启发式合并的经典界）。

和「换根 DP」的区别：
      换根 DP 要算「以每个点为根时的全局答案」，需要**两次** DFS（下 + 上）。
      本题只要「每个点的**子树**答案」，**一次自底向上就够了**。
      看清这个区别，能省掉一半的代码。

边界：
  - 单节点 → `[1]`
  - 链状树（验证不爆栈）
  - 所有标签相同 → `ans[i]` = 子树大小
  - 所有标签不同 → 全是 1
"""

from collections import defaultdict
from typing import List


##################################################################################################
##### ! Solution 1: 迭代后序 DFS + 每节点一张 26 维计数表
##### ! 时间复杂度: O(26 · n)   空间复杂度: O(26 · n)
##### ! 适用：所有「子树统计量自底向上合并」的树上题；用显式栈避免递归深度问题
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def countSubTrees(self, n: int, edges: List[List[int]], labels: str) -> List[int]:
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)                  # ! 无向边
        ans = [0] * n
        counts = [None] * n                   # ! counts[u] = u 子树的 26 维计数表
        # ! 迭代后序：第一遍压栈确定访问顺序，第二遍逆序处理（保证孩子先于父亲）
        order, parent = [], [-1] * n
        stack = [0]
        visited = [False] * n
        visited[0] = True
        while stack:
            u = stack.pop()
            order.append(u)
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    parent[v] = u             # ! 记住父亲，不会走回去
                    stack.append(v)
        for u in reversed(order):             # ! 逆序 = 自底向上
            cnt = [0] * 26
            cnt[ord(labels[u]) - 97] = 1      # ! 先算自己
            for v in adj[u]:
                if v != parent[u]:            # ! 只合并孩子
                    child = counts[v]
                    for i in range(26):
                        cnt[i] += child[i]
                    counts[v] = None          # ! 用完释放，省内存
            counts[u] = cnt
            ans[u] = cnt[ord(labels[u]) - 97]
        return ans


##################################################################################################
##### ! Solution 2: 小表合并进大表（small-to-large / DSU on tree），标签值域任意时的通用解
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：标签不是只有 26 种、而是任意值时；核心是「总是把小的并进大的」
##################################################################################################


class Solution_2:
    def countSubTrees(self, n: int, edges: List[List[int]], labels: str) -> List[int]:
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        ans = [0] * n
        maps = [None] * n
        order, parent = [], [-1] * n
        stack, visited = [0], [False] * n
        visited[0] = True
        while stack:
            u = stack.pop()
            order.append(u)
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    stack.append(v)
        for u in reversed(order):
            cur = defaultdict(int)
            cur[labels[u]] = 1
            for v in adj[u]:
                if v == parent[u]:
                    continue
                child = maps[v]
                maps[v] = None
                # ! 关键：总是把**小的**并进**大的**，否则复杂度退化
                if len(child) > len(cur):
                    cur, child = child, cur
                for key, val in child.items():
                    cur[key] += val
            maps[u] = cur
            ans[u] = cur[labels[u]]
        return ans


##################################################################################################
##### ! Solution 3: 暴力 —— 对每个节点各跑一次子树遍历（基准答案，用来对拍）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n)
##### ! 适用：正确性参照
##################################################################################################


class Solution_3:
    def countSubTrees(self, n: int, edges: List[List[int]], labels: str) -> List[int]:
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        parent = [-1] * n
        stack, visited = [0], [False] * n
        visited[0] = True
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    stack.append(v)
        ans = []
        for root in range(n):
            cnt, st, seen = 0, [root], {root}
            while st:
                u = st.pop()
                if labels[u] == labels[root]:
                    cnt += 1
                for v in adj[u]:
                    if v != parent[u] and v not in seen:
                        seen.add(v)
                        st.append(v)
            ans.append(cnt)
        return ans


if __name__ == "__main__":
    import random

    cases = [(7, [[0, 1], [0, 2], [1, 4], [1, 5], [2, 3], [2, 6]], "abaedcd"),
             (4, [[0, 1], [1, 2], [0, 3]], "bbbb"),
             (1, [], "a"),
             (5, [[0, 1], [0, 2], [1, 3], [0, 4]], "aabab")]
    for n, edges, labels in cases:
        a = Solution_1().countSubTrees(n, [e[:] for e in edges], labels)
        b = Solution_2().countSubTrees(n, [e[:] for e in edges], labels)
        c = Solution_3().countSubTrees(n, [e[:] for e in edges], labels)
        assert a == b == c, (n, edges, labels, a, b, c)
        print(f"n={n}, labels={labels!r} -> {a}")

    # ! 链状树：验证迭代 DFS 不会爆栈
    n = 20000
    chain = [[i, i + 1] for i in range(n - 1)]
    big = Solution_1().countSubTrees(n, chain, "a" * n)
    assert big[0] == n and big[-1] == 1
    print(f"链状树 n={n} 不爆栈 ✓ ans[0]={big[0]}")

    for _ in range(600):                 # ! 随机树三方对拍
        n = random.randint(1, 9)
        edges = [[random.randint(0, v - 1), v] for v in range(1, n)]
        labels = "".join(random.choice("abc") for _ in range(n))
        a = Solution_1().countSubTrees(n, [e[:] for e in edges], labels)
        b = Solution_2().countSubTrees(n, [e[:] for e in edges], labels)
        c = Solution_3().countSubTrees(n, [e[:] for e in edges], labels)
        assert a == b == c, (n, edges, labels, a, b, c)
    print("随机对拍 600 组通过 ✓（26 维表 == 小表合并 == 暴力）")
