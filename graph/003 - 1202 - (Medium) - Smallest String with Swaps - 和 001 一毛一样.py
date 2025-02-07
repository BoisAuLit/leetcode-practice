from typing import List
from collections import defaultdict


class UnionFind:
    def __init__(self, n):
        self.root = list(range(n))
        self.rank = [1] * n
        self.count = n

    def find(self, x: int) -> int:
        if self.root[x] == x:
            return x
        self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x: int, y: int) -> None:
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.root[rootY] = rootX
            elif self.rank[rootY] > self.rank[rootX]:
                self.root[rootX] = rootY
            else:
                self.root[rootY] = rootX
                self.rank[rootX] += 1
            self.count -= 1

    def getCount(self):
        return self.count

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


class Solution:
    def partial_sort(self, strings: List[str], indices: List[int]) -> None:
        chars = sorted([strings[i] for i in indices])
        for index, char in zip(indices, chars):
            strings[index] = char

    def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
        n = len(s)
        unionFind = UnionFind(n)
        for x, y in pairs:
            unionFind.union(x, y)
        for x in range(n):
            unionFind.find(x)
        mapping = defaultdict(list)
        for i in range(n):
            mapping[unionFind.root[i]].append(i)
        strings = list(s)
        for indices in mapping.values():
            self.partial_sort(strings, indices)
        return "".join(strings)


s = Solution()

input_1 = "dcab"

input_2 = [[0, 3], [1, 2], [0, 2]]
result = s.smallestStringWithSwaps(input_1, input_2)

print(result)
