"""LC-1166 - Design File System

Level 1 · 03 Trie 前缀统计与搜索应用 → Level 2 · 02 层级路径与前缀过滤

题目在问：`createPath("/a/b", v)` 只有在**父路径 `/a` 已存在**且 `/a/b` 不存在时才成功；`get(path)` 取值。

### 一句话判据：父路径 = 去掉最后一段

    "/leet/code"  →  父路径 "/leet"       path[:path.rfind('/')]
    "/leet"       →  父路径 ""（根）       根永远「存在」

所以**哈希表就够了**：`createPath` 查父路径在不在、自己在不在，两次 O(1) 查询（字符串哈希摊 O(L)）。
这题被归到 Trie 这一层，是因为它和 LC-1233 Remove Sub-Folders、LC-0588 In-Memory File System 是同一组：
**路径天然是 Trie —— 以 '/' 切开的每一段是一个字符**。哈希表把整条路径当 key，Trie 把每段当一步。

### 哈希表 vs Trie：什么时候 Trie 才有必要

| 操作 | 哈希表 | Trie |
|---|---|---|
| 精确存取（本题全部操作） | O(L) 哈希 | O(段数) 走指针 |
| 列目录 / 删子树 / 前缀统计（LC-0588、LC-1233） | 要扫全表 | **天然支持** |

本题只需精确存取，哈希表是**正确且更简单**的答案；但面试官通常接着问 `ls`、`rm -r`，那就要 Trie。两种都要会。
"""
from typing import Dict, Optional


##################################################################################################
##### ! Solution 1: 哈希表 path → value；父路径 = rfind('/') 之前的部分
##### ! 时间复杂度: createPath / get 均 O(L)（L = 路径长度，哈希要扫一遍字符串）   空间复杂度: O(总字符数)
##### ! 适用：本题的最简正确解。要会解释「为什么父路径一定是 rfind('/') 前面那段」以及根路径的处理
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def __init__(self):
        self.paths: Dict[str, int] = {}

    def createPath(self, path: str, value: int) -> bool:
        if path in self.paths:
            return False
        parent = path[:path.rfind("/")]           # ! "/a/b" → "/a"；"/a" → ""（根）
        if parent and parent not in self.paths:   # ! 空串 = 根，视为永远存在
            return False
        self.paths[path] = value
        return True

    def get(self, path: str) -> int:
        return self.paths.get(path, -1)


##################################################################################################
##### ! Solution 2: Trie —— 每一段路径是一步（为 ls / rm -r 这类追问做准备）
##### ! 时间复杂度: createPath / get O(段数 × 段长)   空间复杂度: O(总字符数)
##### ! 适用：面试官追问「列出目录下所有子项」「删整棵子树」「统计某前缀下的文件数」时，只有 Trie 能 O(子树) 完成。
#####         节点上 value 为 None 表示「只是路径上的中间节点、并未 createPath」—— 本题父路径必须真实存在，所以要区分
##################################################################################################


class _Node:
    __slots__ = ("children", "value")

    def __init__(self):
        self.children: Dict[str, "_Node"] = {}
        self.value: Optional[int] = None


class Solution_2:
    def __init__(self):
        self.root = _Node()

    def createPath(self, path: str, value: int) -> bool:
        parts = path.split("/")[1:]               # ! "/a/b" → ["a", "b"]
        node = self.root
        for seg in parts[:-1]:                    # ! 父路径的每一段都必须是真实创建过的节点
            node = node.children.get(seg)
            if node is None or node.value is None:
                return False
        last = parts[-1]
        if last in node.children:
            return False
        child = _Node(); child.value = value
        node.children[last] = child
        return True

    def get(self, path: str) -> int:
        node = self.root
        for seg in path.split("/")[1:]:
            node = node.children.get(seg)
            if node is None:
                return -1
        return node.value if node.value is not None else -1

    # ! 追问演示：列目录（LC-0588 的 ls）—— 哈希表做不到 O(子项数)
    def ls(self, path: str) -> list:
        node = self.root
        if path != "/":
            for seg in path.split("/")[1:]:
                node = node.children.get(seg)
                if node is None:
                    return []
        return sorted(node.children)


if __name__ == "__main__":
    import random
    random.seed(1166)
    for cls in (Solution_1, Solution_2):
        fs = cls()
        assert fs.createPath("/leet", 1) is True
        assert fs.createPath("/leet/code", 2) is True
        assert fs.get("/leet/code") == 2
        assert fs.createPath("/c/d", 1) is False       # ! 父路径 /c 不存在
        assert fs.get("/c") == -1
        assert fs.createPath("/leet", 9) is False      # ! 已存在
        assert fs.get("/leet") == 1, cls.__name__
    assert Solution_2().ls("/") == []
    fs = Solution_2(); fs.createPath("/a", 1); fs.createPath("/a/x", 2); fs.createPath("/a/b", 3)
    assert fs.ls("/a") == ["b", "x"]

    # ! 随机对拍：两种实现对同一串操作必须给出完全相同的返回值
    segs = ["a", "b", "c"]
    for _ in range(30):
        h, t = Solution_1(), Solution_2()
        for _ in range(400):
            depth = random.randint(1, 3)
            path = "/" + "/".join(random.choice(segs) for _ in range(depth))
            if random.random() < 0.6:
                v = random.randint(1, 99)
                assert h.createPath(path, v) == t.createPath(path, v), path
            else:
                assert h.get(path) == t.get(path), path
    print("所有测试通过 ✓（样例 + 30 × 400 步随机对拍）")
