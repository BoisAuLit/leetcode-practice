"""
Kahn 拓扑排序: 按入度做 BFS

画面:   选课: 先修掉没有先修课的课; 每修完一门, 它后续课程 "还欠的先修课数" 减一, 减到 0 就能修了。
        最后还有课没修到, 说明一群课互相卡住 (有环)。
动作:   ① 数欠账 (indeg[v] = 指向 v 的边数)
        ② 零欠账先修 (indeg == 0 的点全部入队)
        ③ 修完销账 (出队记入 order, 后续课的 indeg 减 1)
        ④ 销到 0 就入队
        ⑤ 验收 (len(order) < n 说明有环)
动作对代码: 见下面 # ! 注释
签名题: LC-207 Course Schedule (能否修完 = 有没有环); LC-210 Course Schedule II (输出 order)
决策句: 有向图问 "先后顺序 / 能否全部完成 / 有没有环" 用它; 要 "最少几学期" 就按层剥 (LC-1136); 要 "哪些点走不进环" 用 07 三色 DFS 更顺手。
改一行: 和 03 BFS 比, 入队条件从 "没访问过" 换成 "indeg 减到 0"; visited 不用了, indeg 就是 visited。
        LC-1136 Parallel Courses: 加一层 for _ in range(len(queue)) 按层剥, 层数就是学期数。
        LC-269 Alien Dictionary: 难点在建图 (相邻单词第一个不同字符连一条边), 建完就是这个模板。
"""
from collections import deque
from typing import List


def topo_order(n: int, edges: List[List[int]]) -> List[int]:
    """edges 里 [u, v] 表示 u 必须排在 v 前面; 有环返回 []"""
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indeg[v] += 1                                   # ! ① 数欠账
    queue = deque(i for i in range(n) if indeg[i] == 0) # ! ② 零欠账先修
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)                                 # ! ③ 修完记入 order
        for v in adj[u]:
            indeg[v] -= 1                               # ! ③ 销账
            if indeg[v] == 0:
                queue.append(v)                         # ! ④ 销到 0 就入队
    return order if len(order) == n else []             # ! ⑤ 验收: 少于 n 个就是有环


def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
    """LC-207: prerequisites 里 [a, b] 表示先修 b 再修 a, 所以边是 b -> a"""
    return len(topo_order(num_courses, [[b, a] for a, b in prerequisites])) == num_courses


def minimum_semesters(n: int, relations: List[List[int]]) -> int:
    """LC-1136: 1-indexed, 每学期可以修所有 indeg 为 0 的课, 问最少几学期; 有环返回 -1"""
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for u, v in relations:
        adj[u].append(v)
        indeg[v] += 1                                   # ! ①
    queue = deque(i for i in range(1, n + 1) if indeg[i] == 0)  # ! ②
    done, semesters = 0, 0
    while queue:
        semesters += 1                                  # ! 按层剥: 一层 = 一学期
        for _ in range(len(queue)):
            u = queue.popleft()
            done += 1                                   # ! ③
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    queue.append(v)                     # ! ④
    return semesters if done == n else -1               # ! ⑤


if __name__ == "__main__":
    print(topo_order(4, [[0, 1], [1, 2], [0, 2], [3, 2]]))      # [0, 3, 1, 2]
    print(can_finish(2, [[1, 0]]))                              # True
    print(can_finish(2, [[1, 0], [0, 1]]))                      # False
    print(minimum_semesters(3, [[1, 3], [2, 3]]))               # 2
    print(minimum_semesters(3, [[1, 2], [2, 3], [3, 1]]))       # -1
