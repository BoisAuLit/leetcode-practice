DP[k][v] = min(DP[k][v], DP[k-1][u], w(u, v))
- Space can be optimized, we only need to iterate E-1 times.

The overview of the DP solution:

Time complexity: O(V·E)
Space complexity: O(V²)

Basic idea:
We use a 2-D array to track the minimum path length from starting node to each other node.
- 0-index line is initialize to baseline.
- 1st line is the path from starting node to all other nodes using at most 1 edge.
- 2nd line is the path form starting node to all other nodes using at most 2 edges.
- ...
- We do this iteration for E-1 times

- The last line is path from starting node to all other nodes using at most E-1 edges.

For the 2-D array.
Row count should be E.
Column count should be V (number of vertices)
