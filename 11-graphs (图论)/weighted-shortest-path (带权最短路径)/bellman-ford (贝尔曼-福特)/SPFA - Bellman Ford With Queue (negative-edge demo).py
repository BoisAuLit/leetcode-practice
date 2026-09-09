# Python3 implementation of SPFA
from collections import deque

graph = [[] for _ in range(100000)]


def addEdge(frm, to, weight):
    graph[frm].append([to, weight])


def print_distance(d, V):
    print("Vertex", "\t", "Distance from source")

    for i in range(1, V + 1):
        print(i, "\t", d[i])

"""
Time complexity:
    O(E) on average
    O(V·E) worst case

Space complexity: O(V)

! In Bellman Ford With Queue program (SPFA)
! Whenever a node is put in queue, we mark it as visited
! Whenever a node is removed from queue, we unmark it as unvisited
"""
def shortestPathFaster(src, V:int):
    dist = [float("inf")] * (V + 1)

    # Boolean array to check if vertex
    # is present in queue or not
    in_queue = [False] * (V + 1)

    dist[src] = 0

    queue = deque()
    queue.append(src)
    in_queue[src] = True

    while len(queue) > 0:
        # Take the front vertex from Queue
        node = queue.popleft()
        in_queue[node] = False
        
        for i in range(len(graph[node])):
            neighbor, weight = graph[node][i]

            if dist[node] + weight < dist[neighbor]:
                dist[neighbor] = dist[node] + weight
                
                if not in_queue[neighbor]:
                    queue.append(neighbor)
                    in_queue[neighbor] = True

    # Print the result
    print_distance(dist, V)


# Driver code
if __name__ == "__main__":
    V = 5
    S = 1

    # Connect vertex a to b with weight w
    # addEdge(a, b, w)

    addEdge(1, 2, 1)
    addEdge(2, 3, 7)
    addEdge(2, 4, -2)
    addEdge(1, 3, 8)
    addEdge(1, 4, 9)
    addEdge(3, 4, 3)
    addEdge(2, 5, 3)
    addEdge(4, 5, -3)

    # Calling shortestPathFaster function
    shortestPathFaster(S, V)

# This code is contributed by mohit kumar 29
