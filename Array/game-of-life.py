"""
Problem Link: https://leetcode.com/problems/game-of-life/

According to Wikipedia's article: "The Game of Life, also known simply as Life, is a cellular automaton devised by the British mathematician John Horton Conway in 1970."

The board is made up of an m x n grid of cells, where each cell has an initial state: live (represented by a 1) or dead (represented by a 0). Each cell interacts with its eight neighbors (horizontal, vertical, diagonal) using the following four rules (taken from the above Wikipedia article):


	Any live cell with fewer than two live neighbors dies as if caused by under-population.
	Any live cell with two or three live neighbors lives on to the next generation.
	Any live cell with more than three live neighbors dies, as if by over-population.
	Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.


The next state of the board is determined by applying the above rules simultaneously to every cell in the current state of the m x n grid board. In this process, births and deaths occur simultaneously.

Given the current state of the board, update the board to reflect its next state.

Note that you do not need to return anything.

 
Example 1:


Input: board = [[0,1,0],[0,0,1],[1,1,1],[0,0,0]]
Output: [[0,0,0],[1,0,1],[0,1,1],[0,1,0]]


Example 2:


Input: board = [[1,1],[1,0]]
Output: [[1,1],[1,1]]


 
Constraints:


	m == board.length
	n == board[i].length
	1 <= m, n <= 25
	board[i][j] is 0 or 1.


 
Follow up:


	Could you solve it in-place? Remember that the board needs to be updated simultaneously: You cannot update some cells first and then use their updated values to update other cells.
	In this question, we represent the board using a 2D array. In principle, the board is infinite, which would cause problems when the active area encroaches upon the border of the array (i.e., live cells reach the border). How would you address these problems?
"""

class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        m, n = len(board), len(board[0])
        for i in range(m):
            for j in range(n):
                if self.canLive(i, j, m, n, board):
                    board[i][j] += 2 if board[i][j] == 0 else 0
                else:
                    board[i][j] += 2 if board[i][j] == 1 else 0
        for i in range(m):
            for j in range(n):
                if board[i][j] == 3:
                    board[i][j] = 0
                elif board[i][j] == 2:
                    board[i][j] = 1

    def canLive(self, i, j, m, n, board) -> bool:
        count1s = 0
        if i + 1 < m and (board[i + 1][j] == 1 or board[i + 1][j] == 3):
            count1s += 1
        if i - 1 > -1 and (board[i - 1][j] == 1 or board[i - 1][j] == 3):
            count1s += 1
        if j + 1 < n and (board[i][j + 1] == 1 or board[i][j + 1] == 3):
            count1s += 1
        if j - 1 > -1 and (board[i][j - 1] == 1 or board[i][j - 1] == 3):
            count1s += 1
        if i + 1 < m and j + 1 < n and (board[i + 1][j + 1] == 1 or board[i + 1][j + 1] == 3):
            count1s += 1
        if i + 1 < m and j - 1 > -1 and (board[i + 1][j - 1] == 1 or board[i + 1][j - 1] == 3):
            count1s += 1
        if i - 1 > -1 and j + 1 < n and (board[i - 1][j + 1] == 1 or board[i - 1][j + 1] == 3):
            count1s += 1
        if i - 1 > -1 and j - 1 > -1 and (board[i - 1][j - 1] == 1 or board[i - 1][j - 1] == 3):
            count1s += 1
        print(f"i:{i};j:{j};count1s:{count1s}")
        if (board[i][j] == 1 or board[i][j] == 3) and count1s < 2:
            return False
        elif (board[i][j] == 1 or board[i][j] == 3) and (count == 2 or count == 3):
            return True
        elif (board[i][j] == 1 or board[i][j] == 3) and count1s > 3:
            return False
        elif (board[i][j] == 0 or board[i][j] == 2) and count1s == 3:
            return True
        else:
            return board[i][j] == 1 or board[i][j] == 3