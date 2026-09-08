from typing import List
import collections


class Solution:
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
