from typing import List
from collections import defaultdict


"""
The description of the algorithm:
 we are asked to check if there exists a path between them.
 If so, we should return the cumulative products along the path as the result.

Dividend: 被除数
Divisor: 除数
Quotient: 商
Remainder: 余数
17÷3=5...2
"""


class Solution:
    def calcEquation(
        self,
        equations: List[List[str]],
        values: List[float],
        queries: List[List[str]],
    ) -> List[float]:
        graph = defaultdict(dict)
        res = []

        for (a, b), val in zip(equations, values):
            graph[a][b] = val
            graph[b][a] = 1 / val

        for a, b in queries:
            res.append(self.backtrack(graph, a, b, 1, set()))

        return res

    def backtrack(self, graph, cur, target, prod, seen):
        if cur not in graph or cur in seen:
            return -1.0

        if cur == target:
            return prod

        seen.add(cur)
        for neighbor, val in graph[cur].items():
            result = self.backtrack(graph, neighbor, target, prod * val, seen)
            if result != -1.0:
                return result

        return -1.0
