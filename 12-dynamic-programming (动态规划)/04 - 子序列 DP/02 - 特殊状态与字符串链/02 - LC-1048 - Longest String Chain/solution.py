from typing import List
from collections import Counter

"""
Time complexity: O()
Space complexity: O()
"""

class Solution:
    
    def isPrefix(self, word1: str, word2: str) -> bool:
        diff_count = 0
        counter1 = Counter(word1)
        counter2 = Counter(word2)
        for letter, count in counter2.items():
            if letter not in Counter(word1):
                diff_count += 1
            elif counter1[letter] != count: 
                diff_count += 1
                
            if diff_count > 1:
                return False
        return True
    
    def longestStrChain(self, words: List[str]) -> int:
        prev_mapping = Counter(words[0])
        prev_word = words[0]

        current_length = max_length = 1
        for word in words[1:]:
            
            
            curr_mapping  = Counter(word)
            if len(word) - len(prev_word) != 1 or not self.isPrefix(prev_mapping, curr_mapping):
                current_length = 1
            else: 
                current_length += 1
                max_length = max(current_length, max_length)
                
            prev_mapping = curr_mapping
            prev_word = word
        return max_length

            
                    

s = Solution()

# ! 这里原本有一行孤立的 `&`（手误留下的字符），会让整个文件 SyntaxError，已删除
input_ = ["a","b","ba","bca","bda","bdca"]
result = s.longestStrChain(input_)
print(result)

