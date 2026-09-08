from typing import List


class Solution:
    def nextGreatestLetter(self, letters: List[str], target: str) -> str:
        left = 0
        right = len(letters) - 1

        while left <= right:
            mid = (left + right) // 2
            if letters[mid] <= target: # 这一步非常关键
                left = mid + 1
            else:
                right = mid - 1

        if left == len(letters):
            return letters[0]
        else:
            return letters[left]


# # Test case 1: Expecting "c"
# s = Solution()
# letters = ["c","f","j"]
# target = "a"
# result = s.nextGreatestLetter(letters, target)
# print(result)

# # Test case 2: Expecting "f"
# s = Solution()
# letters = ["c","f","j"]
# target = "c"
# result = s.nextGreatestLetter(letters, target)
# print(result)

# # Test case 3: Expecting "x" (return first letter)
# s = Solution()
# letters = ["x","x","y","y"]
# target = "z"
# result = s.nextGreatestLetter(letters, target)
# print(result)

# # Test case 4: Expecting "f"
# s = Solution()
# letters = ["c","f","j"]
# target = "d"
# result = s.nextGreatestLetter(letters, target)
# print(result)

# # Test case 5: Expecting "f"
# s = Solution()
# letters = ["c", "f", "j"]
# target = "c"
# result = s.nextGreatestLetter(letters, target)
# print(result)

# Test case 5: Expecting "c"
s = Solution()
letters = ["c", "f", "j"]
target = "a"
result = s.nextGreatestLetter(letters, target)
print(result)
