import heapq

# Create a max heap
# ! Time complexity: O(N)
data = [10, 30, 20, 5, 40, 15]
max_heap = [-x for x in data]
heapq.heapify(max_heap)
print("Max heap after heapify():", [-x for x in max_heap])


# Insert elements into the max heap
# ! Time complexity: O(log(N))
heapq.heappush(
    max_heap, -3
)  # ! Really, don't forget to negete the number for insertion!
heapq.heappush(max_heap, -25)
print("Max Heap after heappush():", [-x for x in max_heap])

# Remove the largest element from the max heap
largest = -heapq.heappop(max_heap)
print("Largest element:", largest)
print("Max Heap after heappop():", [-x for x in max_heap])

"""
Things to take note of:
1. The initial input data must be negated, the negated list is the actual max heap
2. To see the elements in the map heap, we need to negate it back
3. For insertions, we must negate the number for insertion
4. For popping the top element, we must negate the result

"""
