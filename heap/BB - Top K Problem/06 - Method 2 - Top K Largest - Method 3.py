import heapq


def top_k_largest_fast(nums, k):
    """
    时间复杂度: O(n log k)
    空间复杂度: O(k)
    Maintain a min-heap of size k that stores the largest k elements.
    """
    if k <= 0:
        return []
    if k >= len(nums):
        return sorted(nums, reverse=True)  # 如需从大到小输出

    heap = []
    for x in nums:
        if len(heap) < k:
            heapq.heappush(heap, x)
        else:
            heapq.heappushpop(heap, x)  # ⭐️ 下边会有解释
    return sorted(heap, reverse=True)  # 如需从大到小输出


"""
heappushpop 之所以管用, 是应为它的实现如下

当 x <= heap[0]
它不改堆、仅做一次比较就返回，开销是 O(1)。
这和你手写的“先比较、然后啥也不做”的成本相同，并不比你更慢。

当 x > heap[0]
它等价于 heap[0] = x 然后做一次下滤，开销 O(log k),
比“heappop 后再 heappush”通常更省一步上滤/下滤的组合，略快。
"""


def heappushpop(heap, x):
    # 最核心的分支（等价理解）
    if heap and x > heap[0]:
        # 只在 x 比堆顶大时才进行堆的调整（O(log k)）
        smallest = heap[0]
        heap[0] = x
        # _siftdown(heap, 0)  # 下滤
        return smallest
    else:
        # x <= heap[0]：直接返回 x，不改堆（O(1)）
        return x


# --- demo ---
if __name__ == "__main__":
    data = [5, 1, 9, 3, 12, 7, 2, 10, 6, 8, 15, 11, 4, 14, 13]
    print(top_k_largest_fast(data, 5))  # e.g. [15, 14, 13, 12, 11]
