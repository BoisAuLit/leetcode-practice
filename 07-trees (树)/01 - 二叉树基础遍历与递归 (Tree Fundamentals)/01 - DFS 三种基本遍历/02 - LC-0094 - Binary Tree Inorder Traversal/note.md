# Binary Tree Inorder Traversal 笔记

### 📝 2026-10-10 - retry 1

```python
class Solution_Iterative:
    def inorderTraversal(self, root):
        result = []
        stack = []
        curr = root
        while curr or stack: # 这一步非常非常关键
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            result.append(curr.val)
            curr = curr.right
        return result
```
