"""LC-2192 - All Ancestors of a Node in a Directed Acyclic Graph

阶段 3 · Kahn 拓扑排序 —— **沿拓扑序传播「祖先集合」**
题目在问：DAG 中每个节点的**所有祖先**（能到达它的点），升序返回。

点是什么：节点。边是什么：给定的有向边。

决定性观察：
  1. **祖先集合可以沿拓扑序累积**：
     ```
     ancestors[v] = ⋃ ( ancestors[u] ∪ {u} )   对所有边 u → v
     ```
     也就是：v 的祖先 = 所有前驱 u 自己 + u 的全部祖先。
  2. **为什么必须按拓扑序处理**：算 `ancestors[v]` 时需要**所有前驱 u 的结果都已算完**。
     拓扑序恰好保证了「u 一定排在 v 之前」。
     这就是 DAG 上传播信息的通用骨架 —— 和 DAG DP 是同一回事。
  3. Kahn 的流程里，当一条边 `u → v` 被处理（v 的入度减一）时，
     u 的祖先集合已经确定 ⟹ 正好可以在这一刻把 `ancestors[u] ∪ {u}` 并进 v。

```python
indeg = [0] * n
for u, v in edges: adj[u].append(v); indeg[v] += 1
anc = [set() for _ in range(n)]
q = deque(i for i in range(n) if indeg[i] == 0)
while q:
    u = q.popleft()
    for v in adj[u]:
        anc[v] |= anc[u] | {u}        # ★ 传播
        indeg[v] -= 1
        if indeg[v] == 0: q.append(v)
return [sorted(s) for s in anc]
```

复杂度：**O(V·E) 最坏 / O(V² + V·E) 量级** ——
      每条边做一次集合并，集合大小最坏 O(V)。
      题目限制 n ≤ 1000、edges ≤ 2000，可以接受。
      **不要说成 O(V + E)** —— 集合并不是常数操作。

另一种做法（**反向 DFS**，见 Solution_2）：
      对每个节点各跑一次 DFS，看它能到达谁 ⟹ 它就是那些点的祖先。
      复杂度 O(V · (V + E))，实现更直白，常数更小（只用 bool 数组不用 set）。
      两种都值得会，**它们的复杂度量级接近**，选哪个看个人习惯。

输出要**升序** ⟹ 最后 `sorted(...)`。
用「反向 DFS + 按节点编号从小到大发起」的话，祖先天然是升序加入的，可以省掉排序。

边界：
  - 没有边 → 每个节点的祖先都是空列表
  - 链状 DAG（节点 i 的祖先是 0..i-1）
  - 多个入度为 0 的源点
  - n == 1
"""

from collections import deque
from typing import List


##################################################################################################
##### ! Solution 1: Kahn 拓扑序 + 沿边传播祖先集合
##### ! 时间复杂度: O(V·E) 量级（每条边一次集合并）   空间复杂度: O(V^2) 最坏
##### ! 适用：所有「沿 DAG 累积可达性 / 状态」的题；和 DAG DP 是同一个骨架
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def getAncestors(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        adj = [[] for _ in range(n)]
        indeg = [0] * n
        for u, v in edges:
            adj[u].append(v)
            indeg[v] += 1
        anc = [set() for _ in range(n)]
        q = deque(i for i in range(n) if indeg[i] == 0)
        while q:
            u = q.popleft()
            for v in adj[u]:
                anc[v] |= anc[u]        # ! u 的祖先也是 v 的祖先
                anc[v].add(u)           # ! u 自己也是 v 的祖先
                indeg[v] -= 1
                if indeg[v] == 0:       # ! 所有前驱都处理完了，v 的集合才算最终确定
                    q.append(v)
        return [sorted(s) for s in anc]


##################################################################################################
##### ! Solution 2: 对每个点做一次正向 DFS —— 它能到达谁，它就是谁的祖先
##### ! 时间复杂度: O(V · (V + E))   空间复杂度: O(V^2) 输出
##### ! 适用：实现更直白、常数更小（只用 bool 不用 set）；按编号升序发起 ⟹ 结果天然有序
##################################################################################################


class Solution_2:
    def getAncestors(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
        res: List[List[int]] = [[] for _ in range(n)]

        def dfs(src: int, cur: int, seen: List[bool]) -> None:
            for nxt in adj[cur]:
                if not seen[nxt]:
                    seen[nxt] = True
                    res[nxt].append(src)      # ! src 是 nxt 的祖先
                    dfs(src, nxt, seen)

        for src in range(n):                  # ! 按编号升序发起 ⟹ 每个 res[v] 天然升序
            dfs(src, src, [False] * n)
        return res


if __name__ == "__main__":
    import random

    cases = [(8, [[0, 3], [0, 4], [1, 3], [2, 4], [2, 7], [3, 5], [3, 6], [3, 7], [4, 6]]),
             (5, [[0, 1], [0, 2], [0, 3], [0, 4], [1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]),
             (3, []), (1, []), (4, [[0, 1], [1, 2], [2, 3]])]
    for n, edges in cases:
        a = Solution_1().getAncestors(n, [e[:] for e in edges])
        b = Solution_2().getAncestors(n, [e[:] for e in edges])
        assert a == b, (n, edges, a, b)
        print(f"n={n} -> {a}")

    def rand_dag(n):
        """随机 DAG：只允许小编号指向大编号，天然无环。"""
        es = []
        for u in range(n):
            for v in range(u + 1, n):
                if random.random() < 0.35:
                    es.append([u, v])
        return es

    for _ in range(600):
        n = random.randint(1, 8)
        edges = rand_dag(n)
        a = Solution_1().getAncestors(n, [e[:] for e in edges])
        b = Solution_2().getAncestors(n, [e[:] for e in edges])
        assert a == b, (n, edges, a, b)
        for v in range(n):               # ! 输出必须升序
            assert a[v] == sorted(a[v])
    print("随机对拍 600 组通过 ✓（Kahn 传播 == 逐点正向 DFS，且输出升序）")
