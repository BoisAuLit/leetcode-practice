class Solution:
    def answerString(self, word: str, numFriends: int) -> str:
        if numFriends == 1:
            return word
        n = len(word)
        i, j, k = 0, 1, 0
        max_length = n - numFriends + 1
        while j + k < n:
            if word[i + k] == word[j + k]:
                if i + k == n - 1:
                    break
                if k + 1 == max_length:
                    i, j = j, j + 1
                    k = 0
                    continue
                k += 1
                continue
            elif word[i + k] > word[j + k]:
                j = j + k + 1
            else:
                i = max(i + k + 1, j)
                j = i + 1
            k = 0
        return word[i : min(n, i + max_length)]


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
