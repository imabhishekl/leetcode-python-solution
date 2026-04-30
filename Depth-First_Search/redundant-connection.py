"""
Problem Link: https://leetcode.com/problems/redundant-connection/

In this problem, a tree is an undirected graph that is connected and has no cycles.

You are given a graph that started as a tree with n nodes labeled from 1 to n, with one additional edge added. The added edge has two different vertices chosen from 1 to n, and was not an edge that already existed. The graph is represented as an array edges of length n where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the graph.

Return an edge that can be removed so that the resulting graph is a tree of n nodes. If there are multiple answers, return the answer that occurs last in the input.

 
Example 1:


Input: edges = [[1,2],[1,3],[2,3]]
Output: [2,3]


Example 2:


Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
Output: [1,4]


 
Constraints:


	n == edges.length
	3 <= n <= 1000
	edges[i].length == 2
	1 <= ai < bi <= edges.length
	ai != bi
	There are no repeated edges.
	The given graph is connected.
"""

class UF:
    def __init__(self, n):
        self.parent = [0] * (n + 1)
        self.rank = [1] * (n + 1)
        for i in range(n + 1):
            self.parent[i] = i

    def find(self, n) -> int:
        while self.parent[n] != n:
            n = self.parent[n]
        return self.parent[n]

    def union(self, n1, n2) -> bool:
        h1, h2 = self.find(n1), self.find(n2)
        if h1 == h2:
            return False
        elif self.rank[h1] > self.rank[h2]:
            self.parent[h2] = h1
            self.rank[h1] += self.rank[h2]
        else:
            self.parent[h1] = h2
            self.rank[h2] += self.rank[h1]
        return True


class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        uf = UF(n)
        for u, v in edges:
            if not uf.union(u, v):
                return [u, v]
        return []