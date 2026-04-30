"""
Problem Link: https://leetcode.com/problems/alien-dictionary/

There is a new alien language that uses the English alphabet. However, the order of the letters is unknown to you.

You are given a list of strings words from the alien language's dictionary. Now it is claimed that the strings in words are sorted lexicographically by the rules of this new language.

If this claim is incorrect, and the given arrangement of string in words cannot correspond to any order of letters, return "".

Otherwise, return a string of the unique letters in the new alien language sorted in lexicographically increasing order by the new language's rules. If there are multiple solutions, return any of them.

 
Example 1:


Input: words = ["wrt","wrf","er","ett","rftt"]
Output: "wertf"


Example 2:


Input: words = ["z","x"]
Output: "zx"


Example 3:


Input: words = ["z","x","z"]
Output: ""
Explanation: The order is invalid, so return "".


 
Constraints:


	1 <= words.length <= 100
	1 <= words[i].length <= 100
	words[i] consists of only lowercase English letters.
"""

class Solution:
    def alienOrder(self, words: List[str]) -> str:
        result = []
        adj = defaultdict(set)
        indegree = {char: 0 for word in words for char in word}
        for w1, w2 in zip(words, words[1:]):
            print(f"{w1}:{w2}")
            if len(w2) < len(w1) and w1.startswith(w2):
                return ""
            else:
                for c1, c2 in zip(w1, w2):
                    if c1 != c2:
                        if c1 not in adj:
                            adj[c1] = set()
                        adj[c1].add(c2)
                        break
        
        for k, v in adj.items():
            print(f"{k}=>{v}")

        for k, v in adj.items():
            if k not in indegree:
                indegree[k] = 0
            for ch in v:
                if ch not in indegree:
                    indegree[ch] = 0
                indegree[ch] += 1

        q = deque()

        for node, degree in indegree.items():
            print(f"{node}:{degree}")
            if degree == 0:
                q.append(node)

        while q:
            n = q.popleft()
            result.append(n)
            print(f"n<{n}>")
            for nb in adj.get(n, set()):
                indegree[nb] -= 1
                if indegree[nb] == 0:
                    q.append(nb)
        print(f"{"".join(result)}")

        return "" if len(result) < len(indegree) else "".join(result)