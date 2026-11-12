"""LC-0269 - Alien Dictionary

阶段 3 · Kahn（按入度做 BFS） ○ 核心
题目在问：给一组按外星字典序排好的单词，推出这套字母表的顺序；推不出（矛盾 / 有环）返回 ""
点是什么：出现过的每个字母   边是什么：相邻两个单词第一个不同的位置 x != y，给一条 x -> y
和签名题比改了哪一行：207 的边是题目直接给的，这里要自己从相邻单词里"抠"出边；
                     多一个前缀特判：["abc", "ab"] 长的在前直接非法；剩下就是 207 的 Kahn
"""
from typing import List
from collections import defaultdict, deque

##################################################################################################
##### ! Solution 1: Kahn（相邻单词建边 + 按入度 BFS）
##### ! 时间复杂度: O(C + 26 + E)，C = 所有单词的总字符数，E <= 单词数   空间复杂度: O(26 + E)
##### ! 适用：要输出一个合法顺序并顺便判环；多解时任一都对（LeetCode 接受任一合法顺序）
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    # ! LeetCode 的方法名是 alienOrder；NeetCode 上同一题叫 foreignDictionary(self, words)
    def alienOrder(self, words: List[str]) -> str:
        graph = defaultdict(set)
        indegree = {c: 0 for w in words for c in w}  # 所有字母，含孤立的

        for w1, w2 in zip(words, words[1:]):  # 只看相邻对
            for x, y in zip(w1, w2):
                if x != y:
                    if y not in graph[x]:  # 防重复边重复计入度
                        graph[x].add(y)
                        indegree[y] += 1
                    break
            else:  # 没 break：一个是另一个的前缀
                if len(w1) > len(w2):
                    return ""  # 长的在前，非法

        q = deque([c for c in indegree if indegree[c] == 0])
        order = []
        while q:
            c = q.popleft()
            order.append(c)
            for nxt in graph[c]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    q.append(nxt)

        return "".join(order) if len(order) == len(indegree) else ""


##################################################################################################
##### ! Solution 2: 三色 DFS + 后序倒过来
##### ! 时间复杂度: O(C + 26 + E)   空间复杂度: O(26 + E)
##### ! 适用：同样的建边，换 802 的三色 DFS 判环；DFS 的后序（先把所有后继放完再放自己）反过来就是拓扑序
##################################################################################################


class Solution_2:
    def alienOrder(self, words: List[str]) -> str:
        graph = {c: set() for w in words for c in w}
        for w1, w2 in zip(words, words[1:]):
            for x, y in zip(w1, w2):
                if x != y:
                    graph[x].add(y)  # set 自动去重，DFS 也不在乎重边
                    break
            else:
                if len(w1) > len(w2):
                    return ""  # 前缀特判和 Solution 1 一样

        WHITE, GRAY, BLACK = 0, 1, 2
        color = {c: WHITE for c in graph}
        post = []

        def dfs(u: str) -> bool:  # 返回 False = 踩到环
            color[u] = GRAY
            for v in graph[u]:
                if color[v] == GRAY:
                    return False  # ! 灰 = 还在栈上 = 有环
                if color[v] == WHITE and not dfs(v):
                    return False
            color[u] = BLACK
            post.append(u)  # ! 后序：所有后继都放完了才放自己
            return True

        for c in graph:
            if color[c] == WHITE and not dfs(c):
                return ""
        return "".join(reversed(post))  # ! 后序倒过来 = 拓扑序


# ! 期望 "adebc"：只要求 a 在 b 前、b 在 c 前，d / e 位置任意；LeetCode 接受任一合法顺序
s = Solution_1()
words = ["abc", "bcd", "cde"]
result = s.alienOrder(words)
print(result)
