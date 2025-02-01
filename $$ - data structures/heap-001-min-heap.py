import heapq

# Create a list and convert it into a min heap
# ! Time complexity of heapify(): O(N)
data = [10, 30, 20, 5, 40, 15]
heapq.heapify(data)
print(data)


# Insert element into the min heap
# ! Time complexity of heappush(): O(log(N))
heapq.heappush(data, 3)
heapq.heappush(data, 25)
print("Heap after heappush:", data)

# Remove the smallest element from the heap
# ! Time complexity of heappop(): O(log(N))
smallest = heapq.heappop(data)
print("Smallest element", smallest)
print("Heap after heappop():", data)
