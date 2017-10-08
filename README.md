# Sudoku Solver

## About
This was initially written to solve Project Euler problem 96 (solving 50 Sudoku boards), and I am very satisfied with the results. On my machine, it solves each board in an average of 28ms, bringing the total solve time to under 1.5 seconds. I also have not yet encountered a board that this script cannot solve, although I am always on the lookout for new ways to break my code.

The script works by first using _deduction:_ it looks for rows, columns, and sub-grids that can be solved without any guessing. The script loops over the board until no more deductions can be made. Sometimes, this is enough to solve the board completely. In other cases, the only hope is to make some educated guesses.

First the script looks at a cell and determines what possible values can go there. Then, it makes a copy of itself and that list of guesses, and pushes that to a stack. After this "backup" is made, the guess is inserted into the board and the script makes more deductive passes (and potentially more guesses, if needed). If the guesses were correct, then the board will be solved eventually. If not, the copy is popped off of the stack and the next value in the "guess list" is used.

In truth this is a recursive guess-and-check algorithm. It was implemented using a stack to save on space, and to avoid python's lack of tail-call optimization. I believe that this is a reasonable balance of speed and efficiency, but I would be very interested in a highly parallelized version of this code, where all guesses are computed simultaneously. If the overhead of creating all those threads isn't too great, the solution could be found in something proportional to the log of the current time.

## Using the Script
The script runs off of the command line, and takes the name of the file containing the boards as its argument. The format for the file is as follows:

- Each cell is represented by a single numeric digit
- Empty cells are represented as zeros
- There are no spaces in between digits in the same row
- Each row is separated by a line break
- Each board must have a title
- There is no limit to the number of boards you can put in a single file

Check out the included test cases for an example.

The script will output a new text file containing the solved version of each board, or in the event that the board could not be solved, its last guess at the board along with an error message. The program will halt after the board is solved, or after 10,000 guesses.


-Kyle Silver
