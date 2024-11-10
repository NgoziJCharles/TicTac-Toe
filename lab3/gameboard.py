from typing import List
#127.0.0.1
class BoardClass:
    def __init__(self):
        """Initialize the board and statistics."""
        self.username= ''
        self.turn= ''
        self.x_wins = 0
        self.o_wins = 0
        self.o_loses = 0
        self.x_loses = 0
        self.ties = 0
        self.numofgames = 0
        self.board = [[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]]

    def boardgame(self) -> None:
        """Print the current state of the game board."""
        for row in self.board:
            print(*row)

    def resetGameBoard(self) -> None:
        """Reset the game board to the initial state."""
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        self.boardgame()

    def updateGameBoard(self, my_character: int, row: int, col: int) -> None:
        """
        Update the game board with the given character at the specified position.

        Args:
            my_character (int): The character to place on the board (1 for X, 2 for O).
            row (int): The row index (0-2) where the character will be placed.
            col (int): The column index (0-2) where the character will be placed.
        """
        self.board[row][col] = my_character
        self.boardgame()  # calls board

    def boardIsFull(self) -> bool:
        """
        Check if the game board is full.

        Returns:
            bool: True if the board is full, False otherwise.
        """
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        print('Tie Game')
        return True

    def printStats(self) -> None:
        """Print the game statistics."""
        print(f"User: {self.username}")
        print(f"Last Player: {self.turn}")
        print(f"Number of Games: {self.numofgames}")
        print(f"X Wins: {self.x_wins}")
        print(f"O Wins: {self.o_wins}")
        print(f"X Loses: {self.x_loses}")
        print(f"O Loses: {self.o_loses}")
        print(f"Ties: {self.ties}")

    def isWinner(self, player: int) -> bool:
        """
        Check if the specified player has won the game.

        Args:
            player (int): The player character to check for a win (1 for X, 2 for O).

        Returns:
            bool: True if the player has won, False otherwise.
        """
        # Check rows, columns, and diagonals for a win for the specified player character
        for i in range(3):
            # Check rows
            if self.board[i][0] == self.board[i][1] == self.board[i][2] == player:
                return True
            # Check columns
            if self.board[0][i] == self.board[1][i] == self.board[2][i] == player:
                return True

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == player:
            return True

        return False