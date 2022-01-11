from colorama import Fore
from colorama import Style
import os
import sys

# Lets CMD show colors
os.system('')
class Connect_x:
    def __init__(self, win, width, height):
        assert win <= width
        assert win <= height
        assert width >= 2
        assert height >= 2
        self.win = win
        self.width = width
        self.height = height
        self.board = []
        for i in range(self.height):
            col = []
            for k in range(self.width):
                col.append(0)
            self.board.append(col)
    
    # Prints out the game board
    def print_board(self):
        for i in range(self.height):
            if i == 0:
                # for a in range(self.width * 3 + 1):
                #     print("=", end = "")
                print(f"Connect {self.win}")
                print("Enter q to exit anytime!")
                print("")
            for k in range(self.width):
                if self.board[i][k] == 1:
                    print(f"{Fore.BLUE} O {Style.RESET_ALL}", end = "")
                elif self.board[i][k] == 2:
                    print(f"{Fore.RED} O {Style.RESET_ALL}", end = "")
                else:
                    print(f"{Fore.WHITE} O {Style.RESET_ALL}", end = "")
                if k == self.width - 1:
                    print("|")
            if i == self.height - 1:
                for a in range(self.width * 3 + 1):
                    print("=", end = "")
                print("")
        for k in range(self.width):
            if k + 1 >= 10:
                print(f"{Fore.YELLOW} {k + 1}", end = "")
            else:
                print(f"{Fore.YELLOW} {k + 1} ", end = "")
            if k == self.width - 1:
                print(f"| {Style.RESET_ALL}<= Columns")
    
    # Checks available position (row) given a column. Returns None or an integer.
    # col: int
    def check_available_position(self, col):
        if self.board[0][col - 1] != 0:
            return None
        for i in range(self.height):
            if self.board[i][col - 1] != 0:
                return i - 1
        return self.height - 1

    # Adds a piece to the board, given player 1 or 2, and column. Returns either "Win", "No Win", or "Tie" from the resulting move.
    # Requires: player must be either 1 or 2
    # player: int
    # col: int
    def add_piece(self, player, col):
        assert player == 1 or player == 2
        available_position = self.check_available_position(col)
        if available_position is None:
            print("Invalid move. Try again.")
        else:
            self.board[available_position][col - 1] = player
            state = self.check_win(available_position, col)
            return state

    # Returns a list containing numbers from a given column.
    # col: int
    def get_column(self, col):
        column = []
        for i in range(self.height):
            column.append(self.board[i][col - 1])
        return column

    # Returns 2 integers corresponding to the row and column of the topmost and leftmost position on board from the given row and column.
    # row: int
    # col: int
    def get_top_left(self, row, col):
        if row - 1 >= 0 and col - 1 >= 1:
            return self.get_top_left(row - 1, col - 1)
        else:
            return row, col

    # Returns 2 integers corresponding to the row and column of the topmost and rightmost position on board from the given row and column.
    # row: int
    # col: int
    def get_top_right(self, row, col):
        if row - 1 >= 0 and col + 1 <= self.width:
            return self.get_top_right(row - 1, col + 1)
        else:
            return row, col
    
    # Returns a list containing numbers from the top left to bottom right diagonal of the given row and column.
    # row: int
    # col: int
    def get_tl_br(self, row, col):
        diag = []
        tl_row, tl_col = self.get_top_left(row, col)
        curr_row, curr_col = tl_row, tl_col
        while curr_row < self.height and curr_col <= self.width:
            diag.append(self.board[curr_row][curr_col - 1])
            curr_row += 1
            curr_col += 1
        return diag

    # Returns a list containing numbers from the top right to bottom left diagonal of the given row and column.
    # row: int
    # col: int
    def get_tr_bl(self, row, col):
        diag = []
        tr_row, tr_col = self.get_top_right(row, col)
        curr_row, curr_col = tr_row, tr_col
        while curr_row < self.height and curr_col > 0:
            diag.append(self.board[curr_row][curr_col - 1])
            curr_row += 1
            curr_col -= 1
        return diag

    # Checks whether the game is a tie. Returns either True or False
    def check_tie(self):
        for i in range(len(self.board)):
            for k in range(len(self.board[i])):
                if self.board[i][k] == 0:
                    return False
        return True

    # Checks whether there is a win from the given row and column. Returns either "Tie", "win", or "No Win".
    # row: int
    # col: int
    def check_win(self, row, col):
        tie = self.check_tie()
        if tie == True:
            return "Tie"
        row_consecutive = check_longest_consecutive(self.board[row])
        if row_consecutive >= self.win:
            return "Win"
        col_lst = self.get_column(col)
        col_consecutive = check_longest_consecutive(col_lst)
        if col_consecutive >= self.win:
            return "Win"
        diag_tl_br_lst = self.get_tl_br(row, col)
        diag_tl_br_consecutive = check_longest_consecutive(diag_tl_br_lst)
        if diag_tl_br_consecutive >= self.win:
            return "Win"
        diag_tr_bl_lst = self.get_tr_bl(row, col)
        diag_tr_bl_consecutive = check_longest_consecutive(diag_tr_bl_lst)
        if diag_tr_bl_consecutive >= self.win:
            return "Win"
        return "No Win"

def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

# Returns the longest consecutive sequence of identical numbers other than 0 from a given list.
# list1: list
def check_longest_consecutive(list1):
    longest_temp = 1
    longest_final = 1
    for i in range(len(list1)):
        k = 1
        while i + k < len(list1) and list1[i] == list1[i + k] and list1[i] != 0:
            longest_temp += 1
            k += 1
        if longest_temp > longest_final:
            longest_final = longest_temp
        longest_temp = 1
    return longest_final

# Prompts user for input and checks whether it is valid based on the given largest number. Returns a integer.
# largest: int
def get_input(largest):
    while True:
        string = input()
        if string.lower() == "q":
            print("Quitting...")
            quit()
        elif string.isnumeric():
            if largest is None:
                if int(string) <= 0:
                    print("Invalid input. Try again.")
                else:
                    return int(string)
            else:
                if int(string) > largest or int(string) <= 0:
                    print("Invalid input. Try again.")
                else:
                    return int(string)
        else:
            print("Invalid input. Try again.")

if __name__ == '__main__':
    while True:
        print("How many pieces to win?")
        win = get_input(None)
        print("What do you want the width to be? (Must be larger than or equal to the number of pieces to win.)")
        width = get_input(None)
        print("What do you want the height to be? (Must be larger than or equal to the number of pieces to win.)")
        height = get_input(None)
        game = Connect_x(win, width, height)
        clear()
        game.print_board()
        while True:
            print("Player 1: (Enter a column)")
            p1 = get_input(width)
            state = game.add_piece(1, p1)
            clear()
            game.print_board()
            if state == "Win":
                print("Player 1 won!")
                break
            elif state == "Tie":
                print("Tie!")
                break
            
            print("Player 2: (Enter a column)")
            p2 = get_input(width)
            state = game.add_piece(2, p2)
            clear()
            game.print_board()
            if state == "Win":
                print("Player 2 won!")
                break
            elif state == "Tie":
                print("Tie!")
                break
        print("Play again? (y/n)")
        ans = input()
        if ans.lower() == "n":
            quit()
        else:
            continue