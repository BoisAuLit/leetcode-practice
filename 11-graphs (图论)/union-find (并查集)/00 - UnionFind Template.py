"""
Time complexity: 
Union, Find, connected: O(alpha(N))

Space complexity: O(N)
"""

class UnionFind:
    def __init__(self, n):
        self.root = list(range(n)) # Root is the root of each vertex
        self.rank = [1] * n # Rank is height of each vertex
        self.count = n # This is the number of isolated islands

    # The find function here is the same as that in the disjoint set with path compression.
    def find(self, x):
        if x == self.root[x]:
            return x
        # ⭐️⭐️⭐️ 注意这里很容易出错
        # 一定要注意find 的括号里是 self.root[x],
        # 而不是 x, 否则会陷入死循环, 会 stack overflow 的
        self.root[x] = self.find(self.root[x])
        return self.root[x]

    # The union function with union by rank
    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            # * We compare only rank
            # * We change root, we also change rank when equal.
            # ! ⭐️ 注意, 一旦进入了这个 block, 就和 x, y 没有半毛钱关系了
            # ! ⭐️ 就只和 rootX 和 rootY 有关系了
            if self.rank[rootX] > self.rank[rootY]:
                # ! Merge Y-cluster into X-cluster, cuz X is huger
                self.root[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                # ! Merge X-cluster into Y-cluster, cuz Y is huger
                self.root[rootX] = rootY
            else:
                # ! If X-cluster & Y-cluster are of the same size, then 
                # ! we decide that rootX become the new root
                self.root[rootY] = rootX
                self.rank[rootX] += 1
            # Every time we do a union, we decrease islands count by 1
            self.count -= 1 

    # Returns the number of isolated islands
    def getCount(self):
        return self.count
    
    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)
