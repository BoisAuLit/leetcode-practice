from typing import List, Dict


class Solution_Recursion_With_Cache_Worst:
    """
    Time complexity: O(N) --> at most N recursive calls
    Space complexity: O(N) --> Occupied by the cache and recursion
    """
    def getMax(self, nums: List[int], index: int, cache: Dict[int, int]) -> int:
        if index >= len(nums):
            return 0
        if index in cache:
            return cache[index]

        cache[index] = nums[index] + max(
            self.getMax(nums, index + 2, cache),
            self.getMax(nums, index + 3, cache),
        )
        return cache[index]

    def rob(self, nums: List[int]) -> int:
        cache = {}
        return max(self.getMax(nums, 0, cache), self.getMax(nums, 1, cache))



class Solution_DP_Better:
    """
    Time complexity: O(N)
    Space complexity: O(N)
    """
    def rob(self, nums: List[int]) -> int:
        
        # Special handling for empty case.
        if not nums:
            return 0
        
        maxRobbedAmount = [None for _ in range(len(nums) + 1)]
        N = len(nums)
        
        # Base case initialization.
        maxRobbedAmount[N], maxRobbedAmount[N - 1] = 0, nums[N - 1]
        
        # DP table calculations.
        for i in range(N - 2, -1, -1):
            
            # Same as recursive solution.
            maxRobbedAmount[i] = max(maxRobbedAmount[i + 1], maxRobbedAmount[i + 2] + nums[i])
            
        return maxRobbedAmount[0]    
        
class Solution_DP_Best:
    """
    Time complexity: O(N)
    Space complexity: O(1)
    """    
    def rob(self, nums: List[int]) -> int:
        N = len(nums)
        
        rob_next_plus_one = 0
        rob_next = nums[N - 1]
        
        # DP table calculations.
        for i in range(N - 2, -1, -1):
            
            # Same as recursive solution.
            current = max(rob_next, rob_next_plus_one + nums[i])
            
            # Update the variables
            rob_next_plus_one = rob_next
            rob_next = current
            
        return rob_next
