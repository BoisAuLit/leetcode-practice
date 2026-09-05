from typing import List
from collections import defaultdict, deque


class Solution:
    def foreignDictionary(self, words: List[str]) -> str:
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


s = Solution()
words = ["abc", "bcd", "cde"]
result = s.foreignDictionary(words)
print(result)
