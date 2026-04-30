"""
Problem Link: https://leetcode.com/problems/design-add-and-search-words-data-structure/

Design a data structure that supports adding new words and finding if a string matches any previously added string.

Implement the WordDictionary class:


	WordDictionary() Initializes the object.
	void addWord(word) Adds word to the data structure, it can be matched later.
	bool search(word) Returns true if there is any string in the data structure that matches word or false otherwise. word may contain dots '.' where dots can be matched with any letter.


 
Example:


Input
["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
[[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]
Output
[null,null,null,null,false,true,true,true]

Explanation
WordDictionary wordDictionary = new WordDictionary();
wordDictionary.addWord("bad");
wordDictionary.addWord("dad");
wordDictionary.addWord("mad");
wordDictionary.search("pad"); // return False
wordDictionary.search("bad"); // return True
wordDictionary.search(".ad"); // return True
wordDictionary.search("b.."); // return True


 
Constraints:


	1 <= word.length <= 25
	word in addWord consists of lowercase English letters.
	word in search consist of '.' or lowercase English letters.
	There will be at most 2 dots in word for search queries.
	At most 104 calls will be made to addWord and search.
"""

class Trie:
    nodes = None
    isTerminal = False

    def __init__(self, ch):
        self.nodes = {}

    def add(self, v):
        self.nodes[v] = Trie(v)

class WordDictionary:
    root = None

    def __init__(self):
        self.root = Trie('.')

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node.nodes:
                node.add(ch)
            node = node.nodes[ch]
        node.isTerminal = True

    def search(self, word: str) -> bool:
        return self.searchInner(word, self.root)

    def searchInner(self, word: str, node) -> bool:
        for i in range(len(word)):
            ch = word[i]
            if ch in node.nodes:
                node = node.nodes[ch]
            elif ch == '.':
                for c in node.nodes:
                    if self.searchInner(word[i + 1:], node.nodes[c]):
                        return True
                return False
            else:
                return False
        return node.isTerminal

# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)