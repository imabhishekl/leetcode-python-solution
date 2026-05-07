"""
Problem Link: https://leetcode.com/problems/surrounded-regions/

You are given an m x n matrix board containing letters 'X' and 'O', capture regions that are surrounded:


	Connect: A cell is connected to adjacent cells horizontally or vertically.
	Region: To form a region connect every 'O' cell.
	Surround: A region is surrounded if none of the 'O' cells in that region are on the edge of the board. Such regions are completely enclosed by 'X' cells.


To capture a surrounded region, replace all 'O's with 'X's in-place within the original board. You do not need to return anything.

 
Example 1:


Input: board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]

Output: [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]

Explanation:

In the above diagram, the bottom region is not captured because it is on the edge of the board and cannot be surrounded.


Example 2:


Input: board = [["X"]]

Output: [["X"]]


 
Constraints:


	m == board.length
	n == board[i].length
	1 <= m, n <= 200
	board[i][j] is 'X' or 'O'.
"""

class Solution:
    moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        m, n = len(board), len(board[0])
        for i in range(m):
            if board[i][0] == 'O':
                self.traverseDFS(i, 0, m, n, board)
            if board[i][n - 1] == 'O':
                self.traverseDFS(i, n - 1, m, n, board)

        for j in range(n):
            if board[0][j] == 'O':
                self.traverseDFS(0, j, m, n, board)
            if board[m - 1][j] == 'O':
                self.traverseDFS(m - 1, j, m, n, board)

        for i in range(m):
            for j in range(n):
                if board[i][j] == "O":
                    board[i][j] = 'X'
                elif board[i][j] == 'Y':
                    board[i][j] = 'O'

    def traverseDFS(self, i, j, m, n, board) -> None:
        board[i][j] = 'Y'
        for di, dj in self.moves:
            ni, nj = i + di, j + dj
            if ni < m and ni >= 0 and nj < n and nj >= 0 and board[ni][nj] == 'O':
                self.traverseDFS(ni, nj, m, n, board) 