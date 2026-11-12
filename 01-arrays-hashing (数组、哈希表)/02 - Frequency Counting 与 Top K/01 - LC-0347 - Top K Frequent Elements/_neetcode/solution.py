from ast import List
import heapq

class Solution_1_Sorting:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = {}
        for num in nums:
            freq[num] = 1 + freq.get(num, 0)
        another = []
        for num, count in freq.items():
            another.append((count, num))
        another.sort()
        k_count = 0
        result = []
        for i in range(len(another)-1, -1, -1):
            k_count += 1
            result.append(another[i][1])
            if k_count == k:
                return result



class Solution_2_min_heap:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = {}
        for num in nums:
            freq[num] = 1 + freq.get(num, 0)
        min_heap = []
        for num, count in freq.items():
            heapq.heappush(min_heap, (count, num))
            if len(min_heap) > k:
                heapq.heappop(min_heap)
        result = []
        while min_heap:
            result.append(heapq.heappop(min_heap)[1])
        return result

class Solution_3_Bucket_Sort:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        freq = {}
        for num in nums:
            freq[num] = 1 + freq.get(num, 0)
        bucket = [[] for i in range(len(nums) + 1)]
        for num, count in freq.items():
            bucket[count].append(num)
        result = []
        for i in range(len(bucket)-1, -1, -1):
            if len(bucket[i]) > 0:
                for num in bucket[i]:
                    result.append(num)
                    if len(result) == k:
                        return result
