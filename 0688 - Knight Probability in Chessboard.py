class Solution:
    def knightProbability(self, n: int, k: int, row: int, column: int) -> float:
        # Possible moves of the knight
        directions = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        # Initialize a 3D DP array
        dp = [[[0 for _ in range(n)] for _ in range(n)] for _ in range(k + 1)]
        print(dp)
        
        # Base case: probability of being on the board at 0 moves is 1
        dp[0][row][column] = 1

        # Iterate through each step
        for step in range(1, k + 1):
            for r in range(n):
                for c in range(n):
                    if dp[step - 1][r][c] > 0:
                        # Explore all possible knight moves
                        for dr, dc in directions:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < n and 0 <= nc < n:  # Check if on board
                                dp[step][nr][nc] += dp[step - 1][r][c] / 8

        # Sum up the probabilities of being on the board after k moves
        total_probability = sum(dp[k][r][c] for r in range(n) for c in range(n))
        
        return total_probability

# Example usage
solution = Solution()
n = 3
k = 2
row = 0
column = 0
print(solution.knightProbability(n, k, row, column))  # Output: 0.0625
