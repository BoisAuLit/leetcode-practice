"""LC-2097 - Valid Arrangement of Pairs

阶段 6 · 特殊结构 · 欧拉路径 Hierholzer △ 扩展
题目在问：把数对首尾相接排成一列（前一对的 end == 后一对的 start），每一对恰好用一次
点是什么：数对里出现过的数   边是什么：一个数对 [start, end] 就是一条有向边 start → end
和签名题比改了哪一行：332 起点固定 JFK、邻居要按字典序；这里起点要自己找：
    出度比入度多 1 的点（找不到就是欧拉回路，任选一点起步）；邻居不用排序，直接 pop()
核心画面（Hierholzer）：沿着没用过的边一直走，走到死路就把点 append 进 path（后序），
    回溯到还有边的点继续走；最后 path 反转就是欧拉路径，相邻两点连成数对
"""
import sys
from collections import defaultdict
from typing import List

##################################################################################################
##### ! Solution 1: Hierholzer 迭代版（显式栈）
##### ! 时间复杂度: O(E)   空间复杂度: O(V + E)
##### ! 适用：E 到 1e5，一条长链递归会很深，迭代最稳；和 332 迭代版几乎一样，只是起点要先找
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        graph = defaultdict(list)
        degree = defaultdict(int)  # ! 出度 - 入度
        for start, end in pairs:
            graph[start].append(end)
            degree[start] += 1
            degree[end] -= 1

        begin = pairs[0][0]  # ! 没有奇点 = 欧拉回路，从哪开始都行
        for node, d in degree.items():
            if d == 1:  # ! 出度比入度多 1 的点就是路径起点（题目保证有解，所以最多一个）
                begin = node
                break

        stack = [begin]
        path = []  # ! 后序：走到死路的点先进来
        while stack:
            while graph[stack[-1]]:  # ! 栈顶还有没用过的边 → 沿着走，pop() 就是把这条边删掉
                stack.append(graph[stack[-1]].pop())
            path.append(stack.pop())  # ! 死路 → 弹进 path（它一定是路径靠后的点）
        path.reverse()  # ! 后序反转 = 欧拉路径
        return [[path[i], path[i + 1]] for i in range(len(path) - 1)]


##################################################################################################
##### ! Solution 2: Hierholzer 递归版
##### ! 时间复杂度: O(E)   空间复杂度: O(V + E)
##### ! 适用：最好读，和 332 递归版一模一样；递归深度可达 E，要先调递归上限
##################################################################################################


class Solution_2:
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        sys.setrecursionlimit(max(10000, 2 * len(pairs)))  # ! 一条 1e5 长链递归深度就是 1e5

        graph = defaultdict(list)
        degree = defaultdict(int)
        for start, end in pairs:
            graph[start].append(end)
            degree[start] += 1
            degree[end] -= 1

        begin = pairs[0][0]
        for node, d in degree.items():
            if d == 1:
                begin = node
                break

        path = []

        def dfs(node: int) -> None:
            while graph[node]:  # ! 有边就走，pop() 消耗这条边
                dfs(graph[node].pop())
            path.append(node)  # ! 后序入栈

        dfs(begin)
        path.reverse()
        return [[path[i], path[i + 1]] for i in range(len(path) - 1)]


s = Solution_1()
pairs = [[5, 1], [4, 5], [11, 9], [9, 4]]
result = s.validArrangement(pairs)
print(result)  # [[11, 9], [9, 4], [4, 5], [5, 1]]

pairs = [[1, 3], [3, 2], [2, 1]]
result = s.validArrangement(pairs)
print(result)  # [[1, 3], [3, 2], [2, 1]]  （任何合法排列都可以）

pairs = [[1, 2], [1, 3], [2, 1]]
result = s.validArrangement(pairs)
print(result)  # [[1, 2], [2, 1], [1, 3]]
