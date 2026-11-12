"""LC-3403 - Find the Lexicographically Largest String From the Box I

合并自 2 个解法文件:
  1. 002 - 3403 - A(1) - Lexi Maxi String from Box I - Two Pointers 🐢.py
  2. 002 - 3403 - B(1) - Lexi Maxi String from Box I - ChatGPT 🚀.py
"""


# ============================================================================
# Solution 1: Two_Pointers    (原文件: 002 - 3403 - A(1) - Lexi Maxi String from Box I - Two Pointers 🐢.py)
# ============================================================================

input__1 = "dbca"

numFriends_1 = 2

input__1 = "gh"

numFriends_1 = 1

input__1 = "afnn"

numFriends_1 = 3

input__1 = "gllf"

numFriends_1 = 3

input__1 = "afnn"

numFriends_1 = 3

input__1 = "albl"

numFriends_1 = 3

input__1 = "ffmi"

numFriends_1 = 4

class Solution_1_Two_Pointers:
    def answerString(self, word: str, numFriends_1: int) -> str:
        if numFriends_1 == 1:
            return word
        n = len(word)
        i, j, k = 0, 1, 0
        max_length = n - numFriends_1 + 1
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

# ============================================================================
# Solution 2: ChatGPT    (原文件: 002 - 3403 - B(1) - Lexi Maxi String from Box I - ChatGPT 🚀.py)
# ============================================================================

input__2 = "dbca"

numFriends_2 = 2

input__2 = "gh"

numFriends_2 = 1

input__2 = "afnn"

numFriends_2 = 3

input__2 = "gllf"

numFriends_2 = 3

input__2 = "afnn"

numFriends_2 = 3

input__2 = "albl"

numFriends_2 = 3

input__2 = "ffmi"

numFriends_2 = 4

class Solution_2_ChatGPT:
    def answerString(self, word: str, numFriends_2: int) -> str:
        if numFriends_2 == 1:
            return word
        
        n = len(word)
        max_length = n - numFriends_2 + 1
        
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


if __name__ == "__main__":

    # --- Solution 1: Two_Pointers ---
    s = Solution_1_Two_Pointers()
    result = s.answerString(input__1, numFriends_1)
    print(result)
    s = Solution_1_Two_Pointers()
    result = s.answerString(input__1, numFriends_1)
    print(result)
    s = Solution_1_Two_Pointers()
    result = s.answerString(input__1, numFriends_1)
    print(result)
    s = Solution_1_Two_Pointers()
    result = s.answerString(input__1, numFriends_1)
    print()
    print(result)
    s = Solution_1_Two_Pointers()
    result = s.answerString(input__1, numFriends_1)
    print()
    print(result)
    s = Solution_1_Two_Pointers()
    result = s.answerString(input__1, numFriends_1)
    print()
    print(result)
    s = Solution_1_Two_Pointers()
    result = s.answerString(input__1, numFriends_1)
    print()
    print(result)

    # --- Solution 2: ChatGPT ---
    s = Solution_2_ChatGPT()
    result = s.answerString(input__2, numFriends_2)
    print(result)
    s = Solution_2_ChatGPT()
    result = s.answerString(input__2, numFriends_2)
    print(result)
    s = Solution_2_ChatGPT()
    result = s.answerString(input__2, numFriends_2)
    print(result)
    s = Solution_2_ChatGPT()
    result = s.answerString(input__2, numFriends_2)
    print()
    print(result)
    s = Solution_2_ChatGPT()
    result = s.answerString(input__2, numFriends_2)
    print()
    print(result)
    s = Solution_2_ChatGPT()
    result = s.answerString(input__2, numFriends_2)
    print()
    print(result)
    s = Solution_2_ChatGPT()
    result = s.answerString(input__2, numFriends_2)
    print()
    print(result)
