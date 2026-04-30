"""
Problem Link: https://leetcode.com/problems/valid-parenthesis-string/

Given a string s containing only three types of characters: '(', ')' and '*', return true if s is valid.

The following rules define a valid string:


	Any left parenthesis '(' must have a corresponding right parenthesis ')'.
	Any right parenthesis ')' must have a corresponding left parenthesis '('.
	Left parenthesis '(' must go before the corresponding right parenthesis ')'.
	'*' could be treated as a single right parenthesis ')' or a single left parenthesis '(' or an empty string "".


 
Example 1:
Input: s = "()"
Output: true
Example 2:
Input: s = "(*)"
Output: true
Example 3:
Input: s = "(*))"
Output: true

 
Constraints:


	1 <= s.length <= 100
	s[i] is '(', ')' or '*'.
"""

class Solution:
    def checkValidString(self, s: str) -> bool:
        #return self.recurse(s, 0, 0)
        cmax, cmin = 0, 0
        for ch in s:
            if ch == '(':
                cmax += 1
                cmin += 1
            elif ch == ')':
                cmax -= 1
                cmin -= 1
            else:
                cmax += 1
                cmin -= 1
            cmin = max(cmin, 0)
            if cmax < 0:
                return False
        return cmin == 0

    def recurse(self, s: str, index: int, count: int) -> bool:
        print(index)
        if count < 0:
            return False
        elif index == len(s):
            #print(f"cnt:{count}:{count == 0}")
            return count == 0
        if s[index] == '(':
            return self.recurse(s, index + 1, count + 1)
        elif s[index] == ')':
            return self.recurse(s, index + 1, count - 1)
        else:
            op1 = self.recurse(s, index + 1, count + 1)
            op2 = self.recurse(s, index + 1, count - 1)
            op3 = self.recurse(s, index + 1, count)
            #print(f"{op1}:{op2}:{op3}")
            return op1 or op2 or op3