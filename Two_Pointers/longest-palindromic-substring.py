"""
Problem Link: https://leetcode.com/problems/longest-palindromic-substring/

Given a string s, return the longest palindromic substring in s.

 
Example 1:


Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.


Example 2:


Input: s = "cbbd"
Output: "bb"


 
Constraints:


	1 <= s.length <= 1000
	s consist of only digits and English letters.
"""

class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s or len(s) == 1:
            return s
        
        def expandfromcenter(left:int, right:int) -> str:
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return s[left+1:right]
        
        longestpal = ''
        for i in range(len(s)):
            oddpal = expandfromcenter(i,i)
            evenpal = expandfromcenter(i, i+1)
            if len(oddpal) > len(longestpal):
                longestpal = oddpal
            if len(evenpal) > len(longestpal):
                longestpal = evenpal
        return longestpal
