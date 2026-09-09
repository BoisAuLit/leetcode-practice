import heapq

# --- Heap Creation ---
data = [5, 3, 8, 1, 2]
heapq.heapify(data)  # O(n)
print("Min-heap:", data)  # [1, 2, 8, 5, 3] (internal structure, order not sorted)

# --- Insert (push) ---
heapq.heappush(data, 0)  # O(log n)
print("After push:", data)

# --- Get Minimum (peek) ---
print("Minimum element:", data[0])  # O(1)

# --- Remove Minimum (pop) ---
min_val = heapq.heappop(data)  # O(log n)
print("Popped:", min_val, "Heap:", data)

# --- Replace Minimum (pop + push) ---
heapq.heapreplace(data, 6)  # O(log n)
print("After replace:", data)

# --- Push + Pop (more efficient than separate calls) ---
val = heapq.heappushpop(data, 4)  # O(log n)
print("Pushpop result:", val, "Heap:", data)
