"""
Problem Link: https://leetcode.com/problems/walls-and-gates/

You are given an m x n grid rooms initialized with these three possible values.


	-1 A wall or an obstacle.
	0 A gate.
	INF Infinity means an empty room. We use the value 231 - 1 = 2147483647 to represent INF as you may assume that the distance to a gate is less than 2147483647.


Fill each empty room with the distance to its nearest gate. If it is impossible to reach a gate, it should be filled with INF.

 
Example 1:


Input: rooms = [[2147483647,-1,0,2147483647],[2147483647,2147483647,2147483647,-1],[2147483647,-1,2147483647,-1],[0,-1,2147483647,2147483647]]
Output: [[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,4]]


Example 2:


Input: rooms = [[-1]]
Output: [[-1]]


 
Constraints:


	m == rooms.length
	n == rooms[i].length
	1 <= m, n <= 250
	rooms[i][j] is -1, 0, or 231 - 1.
"""

class Solution:
    moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.
        """
        m, n = len(rooms), len(rooms[0])
        q = deque()
        for i in range(m):
            for j in range(n):
                if rooms[i][j] == 0:
                    q.append((i, j))
        while q:
            r, c = q.popleft()
            for dr, dc in self.moves:
                nr = r + dr
                nc = c + dc
                if nr >= 0 and nr < m and nc >= 0 and nc < n and rooms[nr][nc] == 2147483647:
                    rooms[nr][nc] = rooms[r][c] + 1
                    q.append((nr, nc))