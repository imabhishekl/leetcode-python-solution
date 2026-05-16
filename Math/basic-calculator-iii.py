"""
Problem Link: https://leetcode.com/problems/basic-calculator-iii/

Implement a basic calculator to evaluate a simple expression string.

The expression string contains only non-negative integers, '+', '-', '*', '/' operators, and open '(' and closing parentheses ')'. The integer division should truncate toward zero.

You may assume that the given expression is always valid. All intermediate results will be in the range of [-231, 231 - 1].

Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().

 
Example 1:


Input: s = "1+1"
Output: 2


Example 2:


Input: s = "6-4/2"
Output: 4


Example 3:


Input: s = "2*(5+5*2)/3+(6/2+8)"
Output: 21


 
Constraints:


	1 <= s <= 104
	s consists of digits, '+', '-', '*', '/', '(', and ')'.
	s is a valid expression.
"""

class Solution:
    def calculate(self, s: str) -> int:
        q = Deque(s.replace(" ", ""))
        return self.evaluate(q)

    def evaluate(self, q: Deque[str]) -> int:
        num = 0
        stack = []
        sign = '+'
        while q:
            token = q.popleft()
            if token.isdigit():
                num = num * 10 + int(token)
            elif token == '(':
                num = self.evaluate(q)
            if token in "*+-/)" or not q:
                match sign:
                    case '-':
                        stack.append(-num)
                    case '+':
                        stack.append(num)
                    case '*':
                        stack.append(stack.pop() * num)
                    case '/':
                        stack.append(int(stack.pop() / num))
                if token == ')':
                    return sum(stack)
                sign = token
                num = 0
        return sum(stack)