"""LC-0133 - Clone Graph

阶段 0 · 建图、隐式图、状态图 · 显式建图(边列表 → 邻接表) ★ 签名题
题目在问：给一张无向连通图的某个点，深拷贝整张图，返回对应的新点
点是什么：Node 对象   边是什么：node.neighbors(图已经是邻接表形式，不用建)
和签名题(1971)比改了哪一行：seen 数组换成哈希表 old_to_copy(旧点 → 新点)，它同时当 visited 用；
  遍历到一个邻居时，先保证它的克隆存在(没有就新建并入队)，再把克隆接到当前克隆的 neighbors 上
注：5 个 class 已覆盖 DFS 递归 / DFS 迭代 / BFS，没有缺的解法，这次只补 banner 和复杂度
"""
from typing import Optional
from collections import deque


# Definition for a Node.
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


##################################################################################################
##### ! Solution 1: DFS 递归，哈希表 旧点 → 新点
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V)   哈希表 + 递归栈(最深 V 层，n ≤ 100 无妨)
##### ! 适用：最短的写法，面试默写首选；"进来先查表，查不到就建新点、登记、再递归接邻居"
##################################################################################################


class Solution_DFS_Recursive:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:

        old_to_copy = {}

        def dfs(old_node):

            if old_node in old_to_copy:
                return old_to_copy[old_node]

            new_node = Node(old_node.val)
            old_to_copy[old_node] = new_node
            for old_neighbor in old_node.neighbors:
                new_node.neighbors.append(dfs(old_neighbor))

            return new_node

        return dfs(node) if node else None


##################################################################################################
##### ! Solution 2: DFS 迭代(栈)，一趟完成
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V)
##### ! 适用：不想递归时；关键是 "邻居第一次见到就先建克隆并入栈，然后不管见没见过都要接线"
##################################################################################################


class Solution_DFS_Iterative:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:

        if not node:
            return None

        old_to_copy = {node: Node(node.val)}

        stack = [node]

        while stack:
            old_node = stack.pop()

            new_node = old_to_copy[old_node]

            for old_neighbor in old_node.neighbors:
                # 第一次遇到这个邻居：创建它的克隆
                if old_neighbor not in old_to_copy:
                    old_to_copy[old_neighbor] = Node(old_neighbor.val)

                    stack.append(old_neighbor)

                # 将当前克隆节点连接到邻居的克隆节点
                new_node.neighbors.append(old_to_copy[old_neighbor])

        return old_to_copy[node]


##################################################################################################
##### ! Solution 3: BFS 队列，一趟完成
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V)
##### ! 适用：和 Solution 2 只差 popleft；用户原注 preferred，和递归 DFS 并列，这里尊重用户的选择
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################
"""
This is also the preferred solution.
"""


class Solution_BFS_1_Iteration:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:

        if not node:
            return None

        old_to_copy = {node: Node(node.val)}

        queue = deque([node])

        while queue:
            old_node = queue.popleft()

            new_node = old_to_copy[old_node]

            for old_neighbor in old_node.neighbors:
                if old_neighbor not in old_to_copy:
                    old_to_copy[old_neighbor] = Node(old_neighbor.val)

                    queue.append(old_neighbor)

                new_node.neighbors.append(old_to_copy[old_neighbor])

        return old_to_copy[node]


##################################################################################################
##### ! Solution 4: DFS 两趟：先遍历抄出邻接表，再按 val 批量建点接线
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V + E)   多存一份 adj
##### ! 适用：依赖题目保证 "val 恰好是 1..n 且互不相同"，通用图(val 不连续/重复)不能用
##################################################################################################


class Solution_DFS_2_Iterations:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
        if not node:
            return None
        stack = [(node)]
        adj = dict()
        max_ = 0
        while stack:
            node = stack.pop()
            max_ = max(max_, node.val)
            adj[node.val - 1] = [n.val - 1 for n in node.neighbors]
            for n in node.neighbors:
                if n.val - 1 not in adj:
                    stack.append(n)
        nodes = [Node(i + 1) for i in range(max_)]
        for i in range(max_):
            nodes[i].neighbors = [nodes[i] for i in adj[i]]
        return nodes[0]


##################################################################################################
##### ! Solution 5: BFS 两趟：同 Solution 4，遍历换成队列
##### ! 时间复杂度: O(V + E)   空间复杂度: O(V + E)
##### ! 适用：同上，只在 val = 1..n 的前提下成立
##################################################################################################


class Solution_BFS_2_Iterations:
    def cloneGraph(self, node: Optional["Node"]) -> Optional["Node"]:
        if not node:
            return None
        q = deque([node])
        adj = dict()
        max_ = 0
        while q:
            node = q.popleft()
            max_ = max(max_, node.val)
            adj[node.val - 1] = [n.val - 1 for n in node.neighbors]
            for n in node.neighbors:
                if n.val - 1 not in adj:
                    q.append(n)
        nodes = [Node(i + 1) for i in range(max_)]
        for i in range(max_):
            nodes[i].neighbors = [nodes[i] for i in adj[i]]

        return nodes[0]


n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n1.neighbors = [n2]
n2.neighbors = [n1, n3]
n3.neighbors = [n2]
s = Solution_DFS_Recursive()
node = n1
result = s.cloneGraph(n1)
print(result.val)
print(result.neighbors[0].val)
