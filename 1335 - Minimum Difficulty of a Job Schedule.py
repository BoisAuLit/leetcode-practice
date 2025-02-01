from typing import List

class Solution:
    def minDifficulty(self, jobDifficulty: List[int], d: int) -> int:
        if d > len(jobDifficulty):
            return -1
        if d == len(jobDifficulty):
            return sum(jobDifficulty)
        