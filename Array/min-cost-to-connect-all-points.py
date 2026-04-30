"""
Problem Link: https://leetcode.com/problems/min-cost-to-connect-all-points/

You are given an array points representing integer coordinates of some points on a 2D-plane, where points[i] = [xi, yi].

The cost of connecting two points [xi, yi] and [xj, yj] is the manhattan distance between them: |xi - xj| + |yi - yj|, where |val| denotes the absolute value of val.

Return the minimum cost to make all points connected. All points are connected if there is exactly one simple path between any two points.

 
Example 1:


Input: points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
Output: 20
Explanation: 

We can connect the points as shown above to get the minimum cost of 20.
Notice that there is a unique path between every pair of points.


Example 2:


Input: points = [[3,12],[-2,5],[-4,1]]
Output: 18


 
Constraints:


	1 <= points.length <= 1000
	-106 <= xi, yi <= 106
	All pairs (xi, yi) are distinct.
"""

class DSU:
    def __init__(self, nodes):
        self.parents = list(range(nodes))
        self.ranks = [1] * nodes

    def find(self, x):
        if self.parents[x] != x:
            self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            if self.ranks[px] < self.ranks[py]:
                self.parents[px] = py
                self.ranks[py] += self.ranks[px]
            else:
                self.parents[py] = px
                self.ranks[px] += self.ranks[py]
            return True
        return False

class UF:
    def __init__(self, n):
        self.group = [0] * n
        self.rank = [1] * n
        for i in range(n):
            self.group[i] = i

    def find(self, node: int) -> int:
        while self.group[node] != node:
            #self.group[node] = self.find(self.group[node])
            node = self.group[node]
        return self.group[node]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            if self.rank[px] < self.rank[py]:
                self.group[px] = py
                self.rank[py] += self.rank[px]
            else:
                self.group[py] = px
                self.rank[px] += self.rank[py]
            return True
        return False

    def unionV1(self, node1: int, node2: int) -> bool:
        h1, h2 = self.find(node1), self.find(node2)
        if h1 == h2:
            return False
        elif self.rank[h1] < self.rank[h2]:
            self.group[h1] = h2
            self.rank[h2] += self.rank[h1]
        else:
            self.group[h2] = h1
            self.rank[h1] += self.rank[h2]
        return True

class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                dist = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                edges.append((dist, i, j))
        edges.sort()
        #print(f"{edges}")
        uf = UF(n)
        wt, totalEdge = 0, 0
        for dist, n1, n2 in edges:
            if uf.unionV1(n1, n2):
                wt += dist
                totalEdge += 1
                if totalEdge == n - 1:
                    break
        return wt