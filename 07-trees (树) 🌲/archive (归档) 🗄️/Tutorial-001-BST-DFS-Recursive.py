from TreeNode import TreeNode

class DFS_Recursive:
    # ! Left -> Root -> Right
    # ! Expecting "H D I B J E K A L F M C N G O"
    def inorder(self, node: TreeNode):
        if not node:
            return
        self.inorder(node.left)
        print(node.val, end=" ")
        self.inorder(node.right)

    # ! Root -> Left -> Right
    # ! Expecting "A B D H I E J K C F L M G N O"
    def preorder(self, node: TreeNode):
        if not node:
            return
        print(node.val, end=" ")
        self.preorder(node.left)
        self.preorder(node.right)

    # ! Left -> Right -> Root
    # ! Expecting "H I D J K E B L M F N O G C A"
    def postorder(self, node: TreeNode):
        if not node:
            return
        self.postorder(node.left)
        self.postorder(node.right)
        print(node.val, end=" ")

        

s = DFS_Recursive()

treeNode = TreeNode.from_list(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'])
print("Original tree:")
treeNode.printTree()

print("\nInorder Traversal:   ", end=" ")
s.inorder(treeNode)

print("\nPreorder Traversal:  ", end=" ")
s.preorder(treeNode)

print("\nPostorder Traversal: ", end=" ")
s.postorder(treeNode)

