from typing import List
from collections import deque


class Solution:
    def collectTheCoins(self, coins: List[int], edges: List[List[int]]) -> int:
        n = len(coins)

        # ! Edge cases, very important
        if n <= 1:
            return 0

        # ! Build adjacency (as sets so we can remove in O(1))
        # ! Using list is a great choice (better than dict),
        # ! because indices match node numbers
        tree = [set() for _ in range(n)]
        for u, v in edges:
            tree[u].add(v)
            tree[v].add(u)

        total_edges = 2 * (n - 1)  # each undirected edge counted twice
        deleted_edges = 0

        

        

        """
        Initial leaves without coin (deadends)

        As long as an element exists in the queue,
        we are pretty much sure that it's a leaf
        """
        q = deque(i for i in range(n) if len(tree[i]) == 1 and coins[i] == 0)

        # ! 1️⃣ Prune all coinless leaves (deeadends)
        while q:
            curr = q.popleft()
            if not tree[curr]:
                continue
            # ! Since adj[cur] is a set, this is the only way
            # ! to retreive one element from a set
            neig = next(iter(tree[curr]))
            tree[curr].remove(neig)
            tree[neig].remove(curr)
            deleted_edges += 2
            if len(tree[neig]) == 1 and coins[neig] == 0:
                q.append(neig)
        
        """
        Current leaves.

        We are pretty much sure that the current leaves
        must be with coins.

        As long as an element exists in the queue,
        we are pretty much sure that it's a leaf.
        """
        q = deque(i for i in range(n) if len(tree[i]) == 1)
        
        
        """
        2️⃣ From the leaf coin nodes, delete forword 2 edges

        Then we are pretty much sure that the remaining edges
        must be visited twice each to achieve the final result.
        """
        for _ in range(2):
            for _ in range(len(q)):
                """
                We are sure that every time we pop an element
                from the queue, it must be a leaf node
                """
                curr = q.popleft()
                if not tree[curr]:
                    continue
                neig = next(iter(tree[curr]))
                tree[curr].remove(neig)
                tree[neig].remove(curr)
                deleted_edges += 2
                if len(tree[neig]) == 1:
                    q.append(neig)

        return total_edges - deleted_edges
