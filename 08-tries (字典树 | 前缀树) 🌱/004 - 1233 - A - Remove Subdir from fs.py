from typing import List


class Solution:
    def removeSubfolders(self, folder: List[str]) -> List[str]:
        trie = {}
        for word in folder:
            node = trie
            for ch in word.split("/"):
                node = node.setdefault(ch, {})
            node["#"] = word

        res = []
        for word in folder:
            node = trie
            words = word.split("/")
            for i, ch in enumerate(word.split("/")):
                node = node[ch]
                if "#" in node:
                    if i == len(words) - 1:
                        res.append(word)
                    break
        return res


# # Test case 1: Expecting ["/a", "/c/d", "/c/f"]
# s = Solution()
# folder = ["/a", "/a/b", "/c/d", "/c/d/e", "/c/f"]
# result = s.removeSubfolders(folder)
# print(result)

# # Test case 2: Expecting ["/a/b/c", "/a/b/ca", "/a/b/d"]
# s = Solution()
# folder = ["/a/b/c", "/a/b/ca", "/a/b/d"]
# result = s.removeSubfolders(folder)
# print(result)

# Test case 3: Expecting ["/a","/c/d","/c/f"]
s = Solution()
folder = ["/a", "/a/b", "/c/d", "/c/d/e", "/c/f"]
result = s.removeSubfolders(folder)
print(result)
