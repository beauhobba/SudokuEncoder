# SudokuEncoder
A brute force algorithm to try and encode a word into a sudoku. 

## How it Works
When a user enters a sentence, eg "Hello", the sudoku encoder will try and convert this into a decoderable sudoku. Eg:
H = 123, E = 456, L = 789, O = 132.

**Thus:**
1 2 3 4 5 6 7 8 9  
7 8 9 1 3 2 x x x  
x x x x x x x x x  
... 

The encoder creates many combinations for each letter based on its popularity. For example A can be 123, 782, 563 or 213; whilst Z might just be 943. 
