from math import inf as infinity
from random import choice
import platform
import os

class TicTacToe:
    """
    The class that creates the game of Tic Tac Toe.
    """

    def __init__(self):
        """
        Initializes the game with an empty board and sets player markers.
        """
        self.HUMAN = -1
        self.COMP = +1
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.h_choice = ''
        self.c_choice = ''

    def evaluate(self, state):
        """ 
        Evaluates the state of the board to determine the score.
        :param state: the current state of the board
        :return: +1 if COMP wins, -1 if HUMAN wins, 0 otherwise
        """
        if self.wins(state, self.COMP):
            return +1
        elif self.wins(state, self.HUMAN):
            return -1
        return 0

    def wins(self, state, player):
        """ 
        Checks if the player has won.
        :param state: the current state of the board
        :param player: the player to check (HUMAN or COMP)
        :return: True if the player wins, False otherwise
        """
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        return [player, player, player] in win_state

    def game_over(self, state):
        """ 
        Checks if the game is over.
        :param state: the current state of the board
        :return: True if the game is over, False otherwise
        """
        return self.wins(state, self.HUMAN) or self.wins(state, self.COMP)

    def empty_cells(self, state):
        """ 
        Returns a list of empty cells on the board.
        :param state: the current state of the board
        :return: a list of empty cells
        """
        return [[x, y] for x, row in enumerate(state) for y, cell in enumerate(row) if cell == 0]

    def valid_move(self, x, y):
        """ 
        Checks if a move is valid.
        :param x: the x coordinate of the move
        :param y: the y coordinate of the move
        :return: True if the move is valid, False otherwise
        """
        return [x, y] in self.empty_cells(self.board)

    def set_move(self, x, y, player):
        """ 
        Sets a move on the board.
        :param x: the x coordinate of the move
        :param y: the y coordinate of the move
        :param player: the player making the move (HUMAN or COMP)
        :return: True if the move is set, False otherwise
        """
        if self.valid_move(x, y):
            self.board[x][y] = player
            return True
        return False

    def clean(self):
        """ 
        Clears the console.
        """
        os.system('cls' if platform.system().lower() == 'windows' else 'clear')

    def render(self, state, c_choice, h_choice):
        """ 
        Renders the current state of the board.
        :param state: the current state of the board
        :param c_choice: the marker for the computer
        :param h_choice: the marker for the human
        """
        chars = {
            -1: h_choice,
            +1: c_choice,
            0: ' '
        }
        str_line = '---------------'

        print('\n' + str_line)
        for row in state:
            for cell in row:
                symbol = chars[cell]
                print(f'| {symbol} |', end='')
            print('\n' + str_line)

    def human_turn(self, c_choice, h_choice):
        """ 
        Handles the human player's turn.
        :param c_choice: the marker for the computer
        :param h_choice: the marker for the human
        """
        depth = len(self.empty_cells(self.board))
        if depth == 0 or self.game_over(self.board):
            return

        move = -1
        moves = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2],
        }

        self.clean()
        print(f'Human turn [{h_choice}]')
        self.render(self.board, c_choice, h_choice)

        while move < 1 or move > 9:
            try:
                move = int(input('Use numpad (1..9): '))
                coord = moves[move]
                can_move = self.set_move(coord[0], coord[1], self.HUMAN)

                if not can_move:
                    print('Bad move')
                    move = -1
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')

    def start_game(self):
        """ 
        Starts the game by asking the user for choices.
        """
        self.h_choice = self.get_choice('Choose X or O\nChosen: ')
        self.c_choice = 'O' if self.h_choice == 'X' else 'X'

        self.clean()
        first = self.get_choice('First to start?[y/n]: ').upper()

        while len(self.empty_cells(self.board)) > 0 and not self.game_over(self.board):
            if first == 'N':
                self.ai_turn()
                first = ''
            self.human_turn()
            self.ai_turn()

        self.display_result()

    def get_choice(self, prompt):
        """ 
        Asks the user for a choice and returns it.
        :param prompt: the prompt to display to the user
        :return: the user's choice
        """
        choice = ''
        while choice not in ['X', 'O', 'Y', 'N']:
            try:
                choice = input(prompt).upper()
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')
        return choice

    def display_result(self):
        """ 
        Displays the result of the game.
        """
        self.clean()
        self.render(self.board, self.c_choice, self.h_choice)
        if self.wins(self.board, self.HUMAN):
            print('YOU WIN!')
        elif self.wins(self.board, self.COMP):
            print('YOU LOSE!')
        else:
            print('DRAW!')
        exit()

if __name__ == '__main__':
    game = TicTacToe()
    game.start_game()
