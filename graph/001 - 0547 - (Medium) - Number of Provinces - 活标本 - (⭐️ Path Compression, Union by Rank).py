from typing import List


# Union by rank (union() method)
# Path compression (find() method)
"""
Time complexity:
Constructor: O(N)
find(): O(alpha(N))
union(): O(alpha(N))
connected(): O(alpha(N))
"""


class UnionFind:
    def __init__(self, n):
        self.root = list(range(n))
        # Use a rank array to record the height of each vertex, i.e., the "rank" of each vertex.
        # The initial "rank" of each vertex is 1, because each of them is
        # a standalone vertex with no connection to other vertices.
        self.rank = [1] * n
        self.count = n

    # The find function here is the same as that in the disjoint set with path compression.
    def find(self, x):
        if x == self.root[x]:
            return x
        self.root[x] = self.find(self.root[x])
        return self.root[x]

    # The union function with union by rank
    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.root[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
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
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        if not isConnected or len(isConnected) == 0:
            return 0
        n = len(isConnected)
        uf = UnionFind(n)
        for row in range(n):
            for col in range(row + 1, n):
                if isConnected[row][col] == 1:
                    uf.union(row, col)
        return uf.getCount()


s = Solution()

# Test case 1: Expecting 2 (1-2-  3-)
# fmt: off
isConnected = [
    [1, 1, 0],
    [1, 1, 0],
    [0, 0, 1]
]

# Test case 2: Expecting 3 (1-  2-  3-)
isConnected = [
    [1, 0, 0],
    [0, 1, 0], 
    [0, 0, 1]
]

# Test case 3:
isConnected = [
    [1,0,0,1],
    [0,1,1,0],
    [0,1,1,1],
    [1,0,1,1]]
# fmt: on

result = s.findCircleNum(isConnected)
print(result)
