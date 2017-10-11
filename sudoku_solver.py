#!/usr/bin/env python
"""
Solution to Project Euler problem 96 - https://projecteuler.net/problem=96

This project solves Sudoku puzzles by using deduction (eliminating options), and then
using a "guess-and-check" approach when deduction is no longer possible. Although
this could have been done recursively, the decision was made to use an iterative
approach with a stack, since there was no need for branching.
"""

__author__ = "Kyle Silver"
__github__ = "https://github.com/kyleAsilver"

# ####################################################################################
#       STRATEGY:
#       1. Make a pass over the entire board, using "deduction" (process of elimina-
#          -tion)to determine if each blank space can be filled with absolute cert-
#          -ainty (ie there is only one valid option for that space).
#       2. Keep making passes until no more can be made (the board looks the same
#          before and after a pass).
#       3. If deduction can't be used, make a guess and then try using deduction again
#       4. If this guess eventually causes a contradiction on the board, go back to
#          the point when that guess was made, and guess something different
# ####################################################################################

# for dealing with i/o
import sys
import os


class Board(object):
    """contains an internal representation of the board, as well as every method
       needed to solve an incomplete board"""

    # ################################################################################
    #       COMMON FUNCTIONS
    # ################################################################################

    def __init__(self, input_lines):
        """initialize the board"""
        self.board = []  # internal representation of the board
        self.stack = []  # used for making guesses
        for i in input_lines:
            as_int = list(map(int, i))
            self.board.append(as_int)

    def get(self, i, j):
        """returns the value at the given position"""
        return self.board[i][j]

    def insert(self, i, j, value):
        """inserting a value onto the board"""
        self.board[i][j] = value

    def to_string(self):
        """returns a string representation of the board"""
        board_str = ""
        for i in range(0, 9):
            board_str += ''.join(str(e) + " " for e in self.get_row(i))
            board_str += '\n'

        return board_str

    def get_row(self, i):
        """retreive an arbitrary row from the board. numbering is top-to-bottom"""
        return self.board[i]

    def get_column(self, j):
        """retreive an arbitrary column from the board. numbering is left-to-right"""
        return [x_i[j] for x_i in self.board]

    def get_cell(self, cell_index):
        """0 1 2    retreive a 3x3 cell from the board as a list
           3 4 5    meta-cell indexing is the same as regular cell indexinging
           6 7 8    the meta-indexes describe the cell's position on the board"""
        # index calculations
        meta_row_index = (cell_index // 3) * 3
        meta_col_index = (cell_index % 3) * 3

        cell = []
        for i in range(0, 3):
            cell.extend(self.get_row(meta_row_index + i)[meta_col_index: meta_col_index + 3])

        return cell

    # ################################################################################
    #       BOARD VALIDATION
    # ################################################################################

    def is_list_valid(self, test_list):
        """checking a list of 9 entries for repeat non-zero values"""
        element_counts = dict((i, test_list.count(i)) for i in test_list)
        for key, count in element_counts.items():
            if key != 0 and count > 1:
                return False
        return True

    def is_row_valid(self, row_index):
        """checking a specified row for valid entries"""
        return self.is_list_valid(self.get_row(row_index))

    def is_column_valid(self, column_index):
        """checking a specified column for valid entries"""
        return self.is_list_valid(self.get_column(column_index))

    def is_cell_valid(self, cell_index):
        """checking if a given cell is valid"""
        return self.is_list_valid(self.get_cell(cell_index))

    def is_board_valid(self):
        """checking the whole board -- only checks for contradictions"""
        for i in range(0, 9):
            if not(self.is_row_valid(i) and self.is_column_valid(i) and self.is_cell_valid(i)):
                return False
        return True

    def is_solved(self):
        """checking if the board is completely solved"""
        # every space is filled in
        for i in range(0, 9):
            for j in range(0, 9):
                if self.get(i, j) == 0:
                    return False

        # the board is correct
        return self.is_board_valid()

    # ################################################################################
    #       DEDUCTION-BASED DECISIONS
    #       Looks at the board to see if there is only one posible value for a given
    #       position. If so, it fills in that spot on the board
    # ################################################################################

    def get_meta_cell_index(self, i, j):
        """gets the cell index as described above"""
        meta_row_index = i // 3
        meta_column_index = j // 3

        meta_cell_index = (meta_row_index * 3) + meta_column_index
        return meta_cell_index

    def get_valid_entries(self, i, j):
        """given a cell, looks at the enclosing row, column, and cell to determine which
           values would be valid"""
        # error checking
        if self.get(i, j) != 0:
            return [self.get(i, j)]

        # need to make sure the value does not appear in any of these
        row = self.get_row(i)
        column = self.get_column(j)
        cell = self.get_cell(self.get_meta_cell_index(i, j))

        # list of potential values
        results = [x for x in range(1, 10)]

        # removing values
        for i in range(1, 10):
            if i in row or i in column or i in cell:
                results.remove(i)

        return results

    def make_deductive_decision(self, i, j):
        """fills in a spot on the board if it is possible to do it deductively
           returns the number it inserted at the given location
           returns  0 if no decision could be reached
           returns -1 if there are no valid entries (contradiction: mistake in the board)
           returns -2 if the given location was already filled in"""
        # error checking
        if self.get(i, j) != 0:
            return -2

        potential_entries = self.get_valid_entries(i, j)
        if len(potential_entries) > 1:
            return 0
        elif len(potential_entries) == 0:
            return -1
        else:
            # print(potential_entries[0])
            self.insert(i, j, potential_entries[0])
            return potential_entries[0]

    def make_deductive_pass(self):
        """goes over the entire board and makes a deductive decision at each index
           returns the number of times it added a number to the board.
           if there is a contradiction on the board, it halts and returns -1"""
        num_entries = 0
        for i in range(0, 9):
            for j in range(0, 9):
                decision = self.make_deductive_decision(i, j)
                if decision > 0:
                    num_entries += 1
                elif decision == -1:
                    return -1
        return num_entries

    # ################################################################################
    #       GUESS-BASED DECISIONS
    #       When making a deduction-based pass of the board fails to fill in any
    #       values, a guess is made based on a call to get_valid_entries()
    #       That guess is pushed onto a stack (along with the remaining options),
    #       and deduction-based passes are made again until either a contradiction
    #       arises or the board is solved.
    #       Contradictions are handled by popping the board from the stack and
    #       substituting the next value from get_valid_entries()
    # ################################################################################

    class TempBoard(object):
        """a temp-board class for storing guesses.
           holds information relevant to each guess."""

        def __init__(self, board, i_guess, j_guess, valid_entries):
            """stores the values so they can be accessed later"""
            self.board = board
            self.i_guess = i_guess
            self.j_guess = j_guess
            self.valid_entries = valid_entries

    def push_state_to_stack(self, i, j):
        """pushes the current state of the board to a stack.
           used before guesses, and therefore requires the location of the guess.
           returns  1 if a guess can be made
           returns -1 if no guess can be made, but will still push"""
        # getting valid guesses
        valid_entries = self.get_valid_entries(i, j)
        current_board = self.duplicate_board()

        # push to the stack
        self.stack.append(self.TempBoard(current_board, i, j, valid_entries))

        # error checking
        if len(valid_entries) == 0:
            return -1
        else:
            return 1

    def peek(self):
        """returns the last item from the stack without removing it
           returns -1 if there is an error"""
        if len(self.stack) == 0:
            return -1
        else:
            return self.stack[-1]

    def pop(self):
        """removes the last item from the stack and returns it
           returns -1 if there is an error"""
        if len(self.stack) == 0:
            return -1
        else:
            return self.stack.pop()

    def is_equal_to_board(self, other_board):
        """tests to see if two boards are equal"""
        for i in range(0, 9):
            for j in range(0, 9):
                if self.board[i][j] != other_board[i][j]:
                    return False
        return True

    def duplicate_board(self):
        """returns a board with the same values as the current board"""
        new_board = [[0 for j in range(0, 9)]
                     for i in range(0, 9)]
        for i in range(0, 9):
            for j in range(0, 9):
                new_board[i][j] = self.board[i][j]

        return new_board

    def copy_board(self, other_board):
        """returns a copy of an arbitrary board"""
        new_board = [[0 for j in range(0, 9)]
                     for i in range(0, 9)]
        for i in range(0, 9):
            for j in range(0, 9):
                new_board[i][j] = other_board[i][j]

        return new_board

    def make_guess(self, i, j):
        """makes a guess based on the results of get_valid_entries()
           and the current state of the stack
           returns  1 if the guess is made without causing a contradiction
           returns -1 if the guess causes a contradiction"""
        # checking to see if the board is already on the stack
        # if not, pushing it to the stack
        if len(self.stack) == 0 or not(self.is_equal_to_board(self.peek().board)):
            self.push_state_to_stack(i, j)

        # error checking
        valid_entries = self.peek().valid_entries
        if len(valid_entries) == 0:
            return -1

        # placing an uncertain piece on the board
        guess = valid_entries[0]
        self.insert(i, j, guess)

    def roll_back(self):
        """reverts the board to the state it was in at the top of the stack.
           used for un-doing guesses that caused contradictions"""
        # deleting the entry that led to a mistake
        del self.peek().valid_entries[0]

        # if there are no options that work, roll back one step further
        # delete the incorrect guess on that level as well
        while len(self.peek().valid_entries) == 0:
            self.pop()
            del self.peek().valid_entries[0]
            self.board = self.copy_board(self.peek().board)

        # if there are still potential options, try them first
        self.board = self.copy_board(self.peek().board)

    # ################################################################################
    #       SOLVER METHODS
    #       1. Make deductive passes over the board until no more can be made
    #       2. Make a guess at a spot on the board, and continue making
    #          deductive passes
    #       3. If a contradiction is reached, roll back the board one step and
    #          and try a different value
    #       4. Continue this DFS approach until the board is solved
    # ################################################################################

    def find_open_spot(self):
        """finds a blank space on the board, perfect for making guesses"""
        for i in range(0, 9):
            for j in range(0, 9):
                if self.board[i][j] == 0:
                    return i, j
        return -1, -1

    def solve(self):
        """implements the strategy outlined above
           essentially a DFS-style guess-and-check approach"""

        # to prevent infinite loops
        num_steps = 0

        # loop that runs while the board is unsolved
        while num_steps < 10000 and not(self.is_solved()):
            num_steps += 1

            num_deductions = self.make_deductive_pass()
            # if a deductive pass yeilded results, do it again
            if num_deductions > 0:
                continue
            # if there is a contradiction on the board, roll back and try again
            elif num_deductions == -1:
                self.roll_back()
                # make a guess from the rollback spot
                i_guess = self.peek().i_guess
                j_guess = self.peek().j_guess
                self.make_guess(i_guess, j_guess)
            # if there are no contradictions and no further deductions, guess
            # location of this guess is not very important
            else:
                # find a spot to make the guess
                i_guess, j_guess = self.find_open_spot()
                # if there are no spots to make the guess, check if the board is solved
                if i_guess == -1 or j_guess == -1:
                    continue
                # make the guess
                self.make_guess(i_guess, j_guess)

# ####################################################################################
#       CALCULATIONS
# ####################################################################################


# opening and reading the file
try:
    lines = [line.rstrip('\n') for line in open(sys.argv[1])]
except:
    print("File could not be opened")
    sys.exit(0)

# parsing the input data
boards = []
for i in range(0, len(lines), 10):
    input_lines = [lines[i + j] for j in range(1, 10)]
    boards.append(Board(input_lines))

# solving the boards and outputting them to a text file
output_file_name = os.path.splitext(sys.argv[1])[0] + '_solutions.txt'
output_file = open(output_file_name, 'w')

for i in range(0, len(boards)):
    boards[i].solve()
    output_file.write("Board {}: {}".format(i, "SOLVED\n" if boards[i].is_solved() else "COULD NOT BE SOLVED\n"))
    output_file.write(boards[i].to_string())

output_file.close()
