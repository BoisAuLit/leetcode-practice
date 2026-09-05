from typing import List
from collections import deque
import string

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        wordSet = set(wordList)

        # endWord 必须在 wordList 中
        if endWord not in wordSet:
            return 0

        q = deque([beginWord])
        wordSet.discard(beginWord)

        length = 1

        while q:
            for _ in range(len(q)):
                word = q.popleft()

                if word == endWord:
                    return length

                # 尝试修改 word 的每一个位置
                for i in range(len(word)):
                    for ch in string.ascii_lowercase:
                        # 上面已经写了 "if word == endWord:"
                        # 所以这里就没有必要再比了
                        if ch == word[i]:
                            continue

                        nextWord = word[:i] + ch + word[i + 1 :]

                        if nextWord in wordSet:
                            wordSet.remove(nextWord)
                            q.append(nextWord)

            length += 1

        return 0
