class Solution:
    def findTheDifference(self, s: str, t: str) -> str:
        counts = [0] * 26
        a_ascii = ord("a")
        for char in t:
            counts[ord(char) - a_ascii] += 1
        for char in s:
            counts[ord(char) - a_ascii] -= 1
        for index, value in enumerate(counts):
            if value == 1:
                return chr(a_ascii + index)


solution = Solution()
s = "abcd"
t = "abcde"
result = solution.findTheDifference(s, t)
print(result)
