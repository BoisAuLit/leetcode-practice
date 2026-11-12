"""LC-0127 - Word Ladder

阶段 0 · 建图、隐式图、状态图 · 状态图 BFS ○ 核心
题目在问：每次只改一个字母、且中间词必须在 wordList 里，beginWord 最少几步变成 endWord(步数按词数算)；到不了 0
点是什么：一个单词   边是什么：两个词只差一个字母；图不给，要么 26 个字母逐位试，要么用通配符 h*t 分桶
和签名题(752)比改了哪一行：邻居的算法从 "拨一位 ±1" 换成 "换一个字母且在词表里"；
  答案是 "路径上的词数" 所以 length 从 1 起、不是 0；endWord 不在词表直接 0
"""
from typing import List
from collections import deque
from collections import defaultdict
import string

##################################################################################################
##### ! Solution 1: 分层 BFS，邻居 = 逐位换 26 个字母后查词表(用户原版，class 名为 Solution)
##### ! 时间复杂度: O(N · L · 26 · L) = O(26 · N · L²)   空间复杂度: O(N · L)   N = 词数，L = 词长；拼一个候选词要 O(L)
##### ! 适用：最常写、最短的版本；词表当 visited 用，进队就从词表删掉
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution   (和通配符桶并列，选它是因为面试默写最快；N 很大、L 很短时两者一样)
##################################################################################################

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


##################################################################################################
##### ! Solution 2: 通配符分桶 h*t 预建邻居(手册点名的写法)
##### ! 时间复杂度: O(N · L²) 建桶 + O(N · L²) BFS   空间复杂度: O(N · L²)   每个词进 L 个桶，每个 key 长 L
##### ! 适用：想把 "隐式图" 真的建出来的时候；同一个桶里的词两两相邻，省掉 26 倍枚举，L 长时明显更快
##################################################################################################


class Solution_2:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0
        L = len(beginWord)
        buckets = defaultdict(list)  # ! "h*t" → ["hot", "hit", ...]
        for word in wordList:
            for i in range(L):
                buckets[word[:i] + "*" + word[i + 1:]].append(word)

        queue = deque([(beginWord, 1)])
        visited = {beginWord}
        while queue:
            word, length = queue.popleft()
            for i in range(L):
                key = word[:i] + "*" + word[i + 1:]
                for nxt in buckets[key]:  # ! 同桶 = 只差这一位 = 相邻
                    if nxt == endWord:
                        return length + 1
                    if nxt not in visited:
                        visited.add(nxt)
                        queue.append((nxt, length + 1))
                buckets[key] = []  # ! 这个桶扫过一次就清空，避免反复扫
        return 0


##################################################################################################
##### ! Solution 3: 双向 BFS(两头各一个集合，每次扩展小的那头)
##### ! 时间复杂度: O(26 · N · L²) 最坏，实际两个小球比一个大球省很多   空间复杂度: O(N · L)
##### ! 适用：起点终点都已知时的升级版；词表大、分支多时比单向快一个量级
##################################################################################################


class Solution_3:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        wordSet = set(wordList)
        if endWord not in wordSet:
            return 0
        front, back = {beginWord}, {endWord}
        wordSet.discard(beginWord)
        wordSet.discard(endWord)  # ! 两头的起点都不许再被 "发现"
        length = 1
        while front and back:
            if len(front) > len(back):
                front, back = back, front  # ! 永远扩展人少的那一头
            length += 1
            nxt_layer = set()
            for word in front:
                for i in range(len(word)):
                    for ch in string.ascii_lowercase:
                        nxt = word[:i] + ch + word[i + 1:]
                        if nxt in back:
                            return length  # ! 两头相遇
                        if nxt in wordSet:
                            wordSet.remove(nxt)
                            nxt_layer.add(nxt)
            front = nxt_layer
        return 0


s = Solution()
beginWord = "hit"
endWord = "cog"
wordList = ["hot", "dot", "dog", "lot", "log", "cog"]
result = s.ladderLength(beginWord, endWord, wordList)
print(result)  # 5  (hit → hot → dot → dog → cog)
