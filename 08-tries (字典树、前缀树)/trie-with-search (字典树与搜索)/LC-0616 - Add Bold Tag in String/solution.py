from typing import List


class Solution:
    def addBoldTag(self, s: str, words: List[str]) -> str:
        n = len(s)
        
        # Build trie
        trie = {}
        for word in words:
            node = trie
            for ch in word:
                node = node.setdefault(ch, {})
            node["#"] = True

        # Mark bold positions
        bold = [False] * n
        for i in range(n):
            node = trie
            for j in range(i, n):
                if s[j] in node:
                    node = node[s[j]]
                    if "#" in node:
                        for k in range(i, j + 1):
                            bold[k] = True
                else:
                    break

        # Build result - merge consecutive bold/non-bold segments
        result = []
        i = 0
        while i < n:
            j = i
            while j < n and bold[j] == bold[i]:
                j += 1
            word = s[i:j]
            result.append(f"<b>{word}</b>" if bold[i] else word)
            i = j
        
        return "".join(result)


s = Solution()
str_ = "aaabbb"
words = ["aa", "b"]
result = s.addBoldTag(str_, words)
print(result)
