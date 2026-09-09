class Solution:
    def findWords(self, board, words):
        trie = {}
        for word in words:  # 1) 建 Trie
            node = trie
            for ch in word:
                node = node.setdefault(ch, {})
            node["$"] = word  # 结尾存整个单词

        m, n = len(board), len(board[0])
        res = []
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        def dfs(r, c, node):
            ch = board[r][c]
            if ch not in node:  # ★ 剪枝：Trie 里没这个前缀
                return
            nxt = node[ch]
            if "$" in nxt:  # 找到一个完整单词
                res.append(nxt["$"])
                del nxt["$"]  # 去重，避免重复加入
            board[r][c] = "#"  # 标记已访问 ➡️
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] != "#":
                    dfs(nr, nc, nxt) # 🔃
            board[r][c] = ch  # 回溯，恢复 ⬅️

        for r in range(m):
            for c in range(n):
                dfs(r, c, trie)
        return res
