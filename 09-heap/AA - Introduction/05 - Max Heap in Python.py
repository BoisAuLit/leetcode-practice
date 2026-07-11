import heapq

# --- Heap Creation ---
data = [5, 3, 8, 1, 2]
max_heap = [-x for x in data]
heapq.heapify(max_heap)  # O(n)
print("Max-heap (internal):", max_heap)

# --- Insert (push) ---
# When we insert, we must first negate the value
heapq.heappush(max_heap, -10)
print("After push:", max_heap)

# --- Get Maximum (peek) ---
# After retrieving the root, we must negate it
print("Maximum element:", -max_heap[0])  # O(1)

# --- Remove Maximum (pop) ---
# After retrieving the root, we must negate it
max_val = -heapq.heappop(max_heap)  # O(log n)
print("Popped:", max_val, "Heap:", [-x for x in max_heap])

# --- Replace Maximum (pop + push) ---
heapq.heapreplace(max_heap, -7)  # O(log n)
print("After replace:", [-x for x in max_heap])

# --- Push + Pop ---
val = -heapq.heappushpop(max_heap, -9)  # O(log n)
print("Pushpop result:", val, "Heap:", [-x for x in max_heap])
