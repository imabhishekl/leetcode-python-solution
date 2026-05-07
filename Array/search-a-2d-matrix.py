"""
Problem Link: https://leetcode.com/problems/search-a-2d-matrix/

You are given an m x n integer matrix matrix with the following two properties:


	Each row is sorted in non-decreasing order.
	The first integer of each row is greater than the last integer of the previous row.


Given an integer target, return true if target is in matrix or false otherwise.

You must write a solution in O(log(m * n)) time complexity.

 
Example 1:


Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
Output: true


Example 2:


Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
Output: false


 
Constraints:


	m == matrix.length
	n == matrix[i].length
	1 <= m, n <= 100
	-104 <= matrix[i][j], target <= 104
"""

class Solution:
    def getPosition(self, mid, m, n) -> (int, int):
        return (mid // n, mid % n)

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        total = m * n
        l, r = 0, total - 1

        while l <= r:
            mid = l + (r - l) // 2
            cr, cc = self.getPosition(mid, m, n)
            print(f"{l},{r}=>{mid}:{cr},{cc}")
            if matrix[cr][cc] == target:
                return True
            elif target < matrix[cr][cc]:
                r = mid - 1
            else:
                l = mid + 1
        return False