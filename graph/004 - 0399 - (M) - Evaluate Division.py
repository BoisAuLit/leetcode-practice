from typing import List, Tuple
from collections import defaultdict


class UnionFind:
    def __init__(self):
        self.root = []
        self.rank = []
        self.mapping = {}
        self.groups = {}

    def getHash(self, x: str) -> int:
        return self.mapping[x]

    def addIfNeeded(self, x: str) -> int:
        if x not in self.mapping:
            length = len(self.root)
            self.mapping[x] = length
            self.root.append([length, 1])
            self.rank.append(1)

    def find(self, x: int) -> Tuple[int, int]:
        if self.root[x][0] == x:
            return self.root[x]
        parent, ratio = self.root[x]
        self.root[x][0] = self.find(parent)[0]
        self.root[x][1] = self.root[parent][1] * ratio
        return self.root[x]

    def union(self, x: str, y: str, ratio: float) -> None:
        self.addIfNeeded(x)
        self.addIfNeeded(y)

        rootX = self.find(self.getHash(x))[0]
        rootY = self.find(self.getHash(y))[0]

        x_ratio = self.root[self.getHash(x)][1]
        y_ratio = self.root[self.getHash(y)][1]

        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                new_ratio = x_ratio / y_ratio * ratio
                self.root[rootY] = [rootX, new_ratio]
            elif self.rank[rootX] < self.rank[rootY]:
                new_ratio = y_ratio / x_ratio / ratio
                self.root[rootX] = [rootY, new_ratio]
            else:
                new_ratio = x_ratio / y_ratio * ratio
                self.root[rootY] = [rootX, new_ratio]
                self.rank[rootX] += 1

    def connected(self, x: str, y: str) -> bool:
        return self.find(self.getHash(x))[0] == self.find(self.getHash(y))[0]

    def calculate_groups(self) -> None:
        # Expand all trees to the topmost node and update ratios accordingly
        for i in range(len(self.root)):
            self.find(i)
        self.groups = defaultdict(list)
        for index, [root, _] in enumerate(self.root):
            self.groups[root].append(index)

    def query(self, x: str, y: str) -> int:
        if x not in self.mapping or y not in self.mapping:
            return -1
        if not self.connected(x, y):
            return -1
        hashX = self.getHash(x)
        hashY = self.getHash(y)
        if len(self.groups[hashX]) == 1 and hashX == hashY:
            return -1
        return self.find(self.getHash(y))[1] / self.find(self.getHash(x))[1]


class Solution:
    def calcEquation(
        self,
        equations: List[List[str]],
        values: List[float],
        queries: List[List[str]],
    ) -> List[float]:
        unionFind = UnionFind()
        for i in range(len(equations)):
            x, y = equations[i]
            ratio = values[i]
            unionFind.union(x, y, ratio)
            # print(f"Mapping: {unionFind.mapping}")
            # print(f"Root: {unionFind.root}")
            # print(f"Rank: {unionFind.rank}")
            # print("----------------------------------------------")
        unionFind.calculate_groups()
        return [unionFind.query(x, y) for x, y in queries]


s = Solution()

# Test case 1: Expecting [6.00000,0.50000,-1.00000,1.00000,-1.00000]
# equations = [["a", "b"], ["b", "c"]]
# values = [2.0, 3.0]
# queries = [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]]


# Test case 2: Expecting [3.75000,0.40000,5.00000,0.20000]
# equations = [["a", "b"], ["b", "c"], ["bc", "cd"]]
# values = [1.5, 2.5, 5.0]
# queries = [["a", "c"], ["c", "b"], ["bc", "cd"], ["cd", "bc"]]

# Test case 3: Expecting [0.50000,2.00000,-1.00000,-1.00000]
# equations = [["a", "b"]]
# values = [0.5]
# queries = [["a", "b"], ["b", "a"], ["a", "c"], ["x", "y"]]


# Test case 4: Expecting [1.33333,1.00000,-1.00000]
# equations = [["a", "e"], ["b", "e"]]
# values = [4.0, 3.0]
# queries = [["a", "b"], ["e", "e"], ["x", "x"]]

# Test case 5: Expecting [0.66667,0.33333,-1.00000,1.00000,1.00000,0.04464]
# equations = [
#     ["a", "b"],
#     ["c", "b"],
#     ["d", "b"],
#     ["w", "x"],
#     ["y", "x"],
#     ["z", "x"],
#     ["w", "d"],
# ]
# values = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
# queries = [
#     ["a", "c"],
#     ["b", "c"],
#     ["a", "e"],
#     ["a", "a"],
#     ["x", "x"],
#     ["a", "z"],
# ]

# Test case 6: Expecting [2.08791]
equations = [
    ["x1", "x2"],
    ["x3", "x4"],
    ["x2", "x4"],
    ["x10", "x20"],
    ["x30", "x40"],
    ["x20", "x40"],
    ["x4", "x40"],
]
values = [2.0, 3.0, 5.0, 7.0, 11.0, 13.0, 19.0]
queries = [["x1", "x10"]]


result = s.calcEquation(equations, values, queries)
print(result)
