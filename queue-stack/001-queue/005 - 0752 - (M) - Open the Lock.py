from collections import deque


class Solution:
    def openLock(self, deadends: list[str], target: str) -> int:
        dead = set(deadends)
        if "0000" in dead:
            return -1
        if target == "0000":
            return 0
        
        queue = deque([("0000", 0)])
        visited = {"0000"}

        while queue:
            curr, turns = queue.popleft()
            
            if curr == target:
                return turns

            for i in range(4):
                for d in (-1, 1):  # Move up or down
                    new_digit = str((int(curr[i]) + d) % 10)
                    new_combo = curr[:i] + new_digit + curr[i+1:]

                    if new_combo not in visited and new_combo not in dead:
                        visited.add(new_combo)
                        queue.append((new_combo, turns + 1))

        return -1  # If no path found


s = Solution()

# Test case 1: Expecting 6
# deadends = ["0201", "0101", "0102", "1212", "2002"]
# target = "0202"

# Test case 2: Expecting 1
# deadends = ["8888"]
# target = "0009"

# Test case 3: Expecting -1
deadends = ["8887", "8889", "8878", "8898", "8788", "8988", "7888", "9888"]
target = "8888"

# Test case 4: Expecting -1 (when deadends contains "0000")
deadends = ["0000"]
target = "1111"

# Test case 5: Expecting -1 (when deadends doesn't contain "0000" and target is "0000")
deadends = ["1587"]
target = "0000"

result = s.openLock(deadends, target)
print(result)
