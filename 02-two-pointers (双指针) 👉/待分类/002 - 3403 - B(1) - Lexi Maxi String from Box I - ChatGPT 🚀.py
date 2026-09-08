class Solution:
    def answerString(self, word: str, numFriends: int) -> str:
        if numFriends == 1:
            return word
        
        n = len(word)
        max_length = n - numFriends + 1
        
        # Find the maximum character first
        max_char = max(word)
        
        # Only consider positions that start with the maximum character
        candidates = []
        for i in range(n):
            if word[i] == max_char:
                # Ensure we don't exceed the allowed length
                end = min(n, i + max_length)
                candidates.append(word[i:end])
        
        # Return the lexicographically largest candidate
        return max(candidates)


# Test case 1: Expecting "dbc"
s = Solution()
input_ = "dbca"
numFriends = 2
result = s.answerString(input_, numFriends)
print(result)

# Test case 2: Expecting "gh"
s = Solution()
input_ = "gh"
numFriends = 1
result = s.answerString(input_, numFriends)
print(result)

# Test case 3: Expecting "nn"
s = Solution()
input_ = "afnn"
numFriends = 3
result = s.answerString(input_, numFriends)
print(result)

# Test case 4: Expecting "ll"
s = Solution()
input_ = "gllf"
numFriends = 3
result = s.answerString(input_, numFriends)
print()
print(result)

# Test case 5: Expecting "nn"
s = Solution()
input_ = "afnn"
numFriends = 3
result = s.answerString(input_, numFriends)
print()
print(result)

# Test case 6: Expecting "lb"
s = Solution()
input_ = "albl"
numFriends = 3
result = s.answerString(input_, numFriends)
print()
print(result)

# Test case 7: Expecting "m"
s = Solution()
input_ = "ffmi"
numFriends = 4
result = s.answerString(input_, numFriends)
print()
print(result)
