# Binary Tree Right Side View 笔记

### 📝 2026-10-04 - retry 1

```python
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        # level order traversal
        if not root:
            return []
        q = deque([root])
        res = []
        while q:
            res.append(q[-1].val)
            for _ in range(len(q)):
                node = q.popleft()
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
        return res
```
