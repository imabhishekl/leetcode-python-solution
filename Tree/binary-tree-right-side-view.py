"""
Problem Link: https://leetcode.com/problems/binary-tree-right-side-view/

Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.

 
Example 1:


Input: root = [1,2,3,null,5,null,4]

Output: [1,3,4]

Explanation:




Example 2:


Input: root = [1,2,3,4,null,null,null,5]

Output: [1,3,4,5]

Explanation:




Example 3:


Input: root = [1,null,3]

Output: [1,3]


Example 4:


Input: root = []

Output: []


 
Constraints:


	The number of nodes in the tree is in the range [0, 100].
	-100 <= Node.val <= 100
"""

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        result = []
        q = deque()
        if root:
            q.append(root)

        while q:
            size = len(q)
            for i in range(size):
                node = q.popleft()
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
                if i == size - 1:
                    result.append(node.val)
        return result
        