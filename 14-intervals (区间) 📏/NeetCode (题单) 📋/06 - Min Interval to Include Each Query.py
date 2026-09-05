from typing import List
import heapq


class Solution:
    def minInterval(
        self,
        intervals: List[List[int]],
        queries: List[int]
    ) -> List[int]:

        # Sort intervals by left boundary
        intervals.sort()

        # query -> shortest interval length
        answer = {}

        # (interval length, right boundary)
        minHeap = []

        i = 0

        for query in sorted(queries):
            # Add every interval that has already started
            while i < len(intervals) and intervals[i][0] <= query:
                left, right = intervals[i]

                heapq.heappush(
                    minHeap,
                    (right - left + 1, right)
                )

                i += 1

            # Remove intervals that ended before query
            """
            只把 heap 顶部已经过期的 interval 不断删掉，直到 heap 顶部是一个仍然有效的 interval。
            并不能保证一次性把所有过期的 intervals (即 end < 当前 query 的) 都删掉,
            这个叫作 lazy deletion

            但是这个操作能保证 minHeap[0] 永远是长度最短并且 ending >= query 的 (符合要求的)
            """
            while minHeap and minHeap[0][1] < query:
                heapq.heappop(minHeap)

            # Smallest valid interval
            if minHeap:
                answer[query] = minHeap[0][0]
            else:
                answer[query] = -1

        # Restore original query order
        return [answer[query] for query in queries]
