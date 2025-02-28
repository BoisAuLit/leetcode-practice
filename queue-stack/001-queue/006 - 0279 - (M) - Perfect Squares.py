class Solution:
    def numSquares(self, n):
        # list of square numbers that are less than `n`
        square_nums = [i * i for i in range(1, int(n**0.5) + 1)]

        level = 0
        queue = {n}
        while queue:
            level += 1
            #! Important: use set() instead of list() to eliminate the redundancy,
            # which would even provide a 5-times speedup, 200ms vs. 1000ms.
            next_queue = set()
            # construct the queue for the next level
            for remainder in queue:
                for square_num in square_nums:
                    if remainder == square_num:
                        return level  # find the node!
                    elif remainder < square_num:
                        break
                    else:
                        next_queue.add(remainder - square_num)
            queue = next_queue
        return level


s = Solution()

# Test case 1: Expecting 3 (12 = 4 + 4 + 4)
# n = 12

# Test case 2: Expecting 2 (13 = 4 + 9)
n = 13

result = s.numSquares(n)
print(result)
