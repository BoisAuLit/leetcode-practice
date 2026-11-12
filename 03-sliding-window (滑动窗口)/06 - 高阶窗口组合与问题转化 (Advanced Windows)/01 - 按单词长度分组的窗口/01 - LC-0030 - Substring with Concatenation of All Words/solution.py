"""LC-0030 - Substring with Concatenation of All Words

合并自 2 个解法文件:
  1. 001 - 0030 - A - Substring Concat All Words.py
  2. 001 - 0030 - B - Substring Concat All Words.py
"""

from typing import List

import collections


# ============================================================================
# Solution 1: A    (原文件: 001 - 0030 - A - Substring Concat All Words.py)
# ============================================================================

# Time complexity: O(n·a·b - (a·b)²)
# Space complexity: O(a+b)

str_ = "aaa"

words = ["a", "a"]

class Solution_1_A:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        n = len(s)
        k = len(words)
        word_length = len(words[0])
        substring_size = word_length * k
        word_count = collections.Counter(words)

        def check(i):
            # Copy the original dictionary to use for this index
            remaining = word_count.copy()
            words_used = 0

            # Each iteration will check for a match in words
            for j in range(i, i + substring_size, word_length):
                sub = s[j : j + word_length]
                if remaining[sub] > 0:
                    remaining[sub] -= 1
                    words_used += 1
                else:
                    break

            # Valid if we used all the words
            return words_used == k

        answer = []
        for i in range(n - substring_size + 1):
            if check(i):
                answer.append(i)

        return answer

# ============================================================================
# Solution 2: B    (原文件: 001 - 0030 - B - Substring Concat All Words.py)
# ============================================================================

class Solution_2_B:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        n = len(s)
        nb_words = len(words)
        word_length = len(words[0])  # Every word has the same length
        substring_size = word_length * nb_words
        word_count = collections.Counter(words)

        def sliding_window(left):
            # Keep track of the words found so far in a python Counter
            words_found = collections.defaultdict(int)
            """
            Keep track of the total of words used so far.
            When words_used == nb_words, it doesn't necessarily mean we have a good match
            it can also mean that there's an excess word.
            """
            words_used = 0
            # Indicates wether we encounter an excess word
            excess_word = False

            # iterate word_length at a time, we focus on one word every time
            for right in range(left, n, word_length):
                if right + word_length > n:  # Meaning out of range
                    break

                # This is the current word
                current_word = s[right : right + word_length]

                # ! This is case 1: current word is not in the dictionary
                if current_word not in word_count:
                    # Mismatched word - reset the window
                    words_found = collections.defaultdict(int)
                    words_used = 0
                    excess_word = False
                    left = right + word_length  # Retry at the next index
                else:
                    """
                    For case 2: there's an excess word
                    - We will continue until the excess word is removed from current sliding window

                    For case 3: The current window size is the expected total dictionary words size
                    - We will just move forward one word!
                    """
                    while right - left == substring_size or excess_word:
                        # Move the left bound over continously
                        leftmost_word = s[left : left + word_length]
                        left += word_length
                        words_found[leftmost_word] -= 1

                        if (
                            words_found[leftmost_word]
                            == word_count[leftmost_word]
                        ):
                            # ! The leftmost word was the excess word
                            excess_word = False
                        else:
                            # Otherwise we actually needed it
                            words_used -= 1

                    # Keep track of how many times this word occurs in the window
                    words_found[current_word] += 1
                    if words_found[current_word] <= word_count[current_word]:
                        words_used += 1
                    else:
                        # Found too many instances already
                        excess_word = True

                    if words_used == nb_words and not excess_word:
                        # Found a valid substring
                        answer.append(left)

        answer = []
        for i in range(word_length):
            sliding_window(i)

        return answer


if __name__ == "__main__":

    # --- Solution 1: A ---
    s = Solution_1_A()
    result = s.findSubstring(str_, words)
    print(result)
