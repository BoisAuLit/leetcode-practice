from typing import List, Tuple
from collections import defaultdict, deque

"""
Special cases to take care of:

! Take care of this in get_dep() function
1. Input is ["ad", "adc"]
- From these two words, there's nothing that we can deduct from

! Take care of this in get_dep() function
2. Input is ["adc", "ad"]
- This is impossible, because words sharing the same prefixes must have
shorter word come fist! Because ⦰ < [any letter]

3. Input is ["adc"]
- If input is only one word, then just return it.

4. Input is ["aba"]
- In the output there must only be unique letters!
"""


class Solution:
    def alienOrder(self, words: List[str]) -> str:
        if len(words) == 1:
            return "".join(set(words[0]))

        def get_dep(word1: str, word2: str) -> Tuple[str, str, bool]:
            n1 = len(word1)
            n2 = len(word2)
            i = 0

            while True:
                # word1 and word2 share common prefix
                # word2 is longer than word1
                # From here
                # ! we can deduct nothing interesting
                if i >= n1 and i <= n2 - 1:
                    return -1, -1, False
                
                # word1 and word2 share common prefix
                # word1 is longer than word2
                # From here we can deduct that 
                # ! we should terminate
                if i <= n1 - 1 and i >= n2:
                    return -1, -1, True
                # word1 == word2
                if i >= n1 and i >= n2:
                    return -1, -1, False

                if word1[i] == word2[i]:
                    i += 1
                    continue
                else:
                    return word1[i], word2[i], False

        all_letters = set()
        graph = defaultdict(set)
        in_degree = defaultdict(int)
        encountered_in_degrees = set()
        for i in range(len(words) - 1):
            curr_word = words[i]
            next_word = words[i + 1]
            all_letters.update(curr_word)
            if i == len(words) - 2:
                all_letters.update(next_word)
            x, y, should_terminate = get_dep(curr_word, next_word)
            if should_terminate:
                return ""
            if x == -1:
                continue
            graph[x].add(y)
            if (x, y) not in encountered_in_degrees:
                encountered_in_degrees.add((x, y))
                in_degree[y] += 1

        # ! This is very important, for special case ['z', 'z']
        if len(all_letters) == 1:
            return list(all_letters)[0]

        queue = deque()  # Letters without prerequisites
        for letter in all_letters:
            if letter not in in_degree:
                queue.append(letter)

        index = 0
        order = [0] * len(all_letters)
        while queue:
            node = queue.popleft()
            order[index] = node
            index += 1
            for neigh in graph[node]:
                in_degree[neigh] -= 1
                if in_degree[neigh] == 0:
                    queue.append(neigh)
        if index != len(all_letters):
            return ""
        return "".join(order)


# Test case 1: Expecting wertf
# s = Solution()
# words = ["wrt", "wrf", "er", "ett", "rftt"]
# result = s.alienOrder(words)
# print(result)

# Test case 2: Expecting "z"
# s = Solution()
# words = ["z", "z"]
# result = s.alienOrder(words)
# print(result)


# Test case 3: Expecting ...
# s = Solution()
# words = ["wrt","wrtkj"]
# result = s.alienOrder(words)
# print(result)

# Test case 4: Expecting "acbz"
# s = Solution()
# words = ["ac", "ab", "zc", "zb"]
# result = s.alienOrder(words)
# print(result)

# Test case 5: Expecting ""
s = Solution()
words = ["abc", "ab"]
result = s.alienOrder(words)
print(result)
