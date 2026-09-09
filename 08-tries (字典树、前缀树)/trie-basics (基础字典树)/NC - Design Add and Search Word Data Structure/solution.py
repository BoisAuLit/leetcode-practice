"""
"到头看 #，遇点试所有孩子，普通字符在就往下走。"
"""

class WordDictionary:
    def __init__(self):
        self.trie = {}

    def addWord(self, word: str) -> None:
        node = self.trie
        for ch in word:
            node = node.setdefault(ch, {})
        node["#"] = word

    def search(self, word: str) -> bool:
        node = self.trie
        nodes = [node]
        for ch in word:
            tmp = []
            if ch == ".":
                for node in nodes:
                    if list(node.keys()) == ["#"]:
                        continue
                    tmp.extend(node.values())
            else:
                for node in nodes:
                    if list(node.keys()) == ["#"]:
                        continue
                    if ch not in node:
                        continue
                    tmp.append(node[ch])
            nodes = tmp
            if not nodes:
                return False
        return any("#" in x for x in nodes)


# =========================================================================
# Solution B - 递归 DFS (更简洁的写法，与上面的 BFS 版功能完全等价)
# 想用哪个版本，把对应的 class 名改成 WordDictionary 即可。
# =========================================================================
class WordDictionary_DFS:
    def __init__(self):
        self.trie = {}

    def addWord(self, word: str) -> None:
        node = self.trie
        for ch in word:
            node = node.setdefault(ch, {})
        node["#"] = word

    def search(self, word: str) -> bool:
        def dfs(node, i):
            if i == len(word):  # 走完 word → 看是否是完整单词
                return "#" in node
            ch = word[i]
            if ch == ".":  # 通配：任一非终止子节点能匹配即可
                return any(dfs(child, i + 1) for k, child in node.items() if k != "#")
            return ch in node and dfs(node[ch], i + 1)  # 普通字符：存在且后续匹配

        return dfs(self.trie, 0)


# wd = WordDictionary()
# wd.addWord("day")
# wd.addWord("bay")
# wd.addWord("may")
#
# print(f"\tsay = {wd.search('say')}")
# print()
# print(f"\tday = {wd.search('day')}")
# print()
# print(f"\t.ay = {wd.search('.ay')}")
# print()
# print(f"\tb.. = {wd.search('b..')}")
# print()

wd = WordDictionary()
wd.addWord("communication")
wd.addWord("communion")
wd.addWord("community")
wd.addWord("commute")

print(f"\tcommuni..ion = {wd.search('communi..ion')}")
print()
# print(f"\tcom..ty = {wd.search('com..ty')}")
# print()
# print(f"\tc..e = {wd.search('c..e')}")
# print()


# wordDictionary = WordDictionary()
# wordDictionary.addWord("day")
# wordDictionary.addWord("bay")
# wordDictionary.addWord("may")
# print("\t🤩 say =", wordDictionary.search("say"))  # return false
# print()
# print("\t🤩 day =", wordDictionary.search("day"))  # return true
# print()
# print("\t🤩 .ay =", wordDictionary.search(".ay"))  # return true
# print()
# print("\t🤩 b.. =", wordDictionary.search("b.."))  # return true
