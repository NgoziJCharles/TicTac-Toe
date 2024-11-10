import socket
from gameboard import BoardClass

#127.0.0.1
tt = BoardClass()
def game_status(tt: BoardClass) -> bool:
    """
    Check the game status to determine if there's a winner or if the board is full.

    Args:
        tt (BoardClass): The game board instance.

    Returns:
        bool: True if the game should continue, False otherwise.
    """
    my_character = 'x'
    opponent = 'o'
    if tt.isWinner(my_character):
        print('You Won!')
        tt.x_wins += 1
        tt.o_loses += 1
        tt.turn = 'Player 1'
        return False
    elif tt.isWinner(opponent):
        print('Player 2 Won!')
        tt.o_wins += 1
        tt.x_loses += 1
        tt.turn = 'Player 2'
        return False
    if tt.boardIsFull():
        tt.ties += 1
        return False
    tt.username = 'Player 1'
    return True

def play_game(conn: socket.socket, tt: BoardClass) -> None:
    """
    Play the game of Tic-Tac-Toe between Player 1 and Player 2.

    Args:
        conn (socket.socket): The socket connection to the other player.
        tt (BoardClass): The game board instance.
    """
    print('Instructions:')
    print('  1. You will use the numbers 0-2. 0 is the first row, 1 the second row, and 2 the third row. It is the same for columns.')
    print('  2. Your input should be structured like "0 1" with a space ONLY in between the numbers. Have Fun!')

    while True:
        tt.resetGameBoard()
        game_active = True
        my_character = 'x'
        opponent_character = 'o'
        tt.numofgames += 1

        while game_active:
            my_move = input("Enter a row and column w/ a space in between (or 'q' to quit): ")
            if my_move.lower() == 'q':
                conn.send('q'.encode())
                print("You quit the game.")
                game_active = False
                break

            if not game_status(tt):
                game_active = False
                continue

            try:
                row, col = map(int, my_move.split())
                if row not in [0, 1, 2] or col not in [0, 1, 2]:
                    print('Number is not valid, try again')
                    continue
                elif tt.board[row][col] != 0:
                    print('Invalid move, try again')
                    continue
                else:
                    tt.updateGameBoard(my_character, row, col)
                    conn.send(f"{row} {col}".encode())
            except ValueError:
                print("Not a valid input. Try again")
                continue

            if not game_status(tt):
                game_active = False
                continue

            data = conn.recv(1024).decode()
            if data == 'q':
                print('Player 2 quit. Thank you for playing!')
                game_active = False
                break

            if not data:
                break

            row, col = map(int, data.split())
            print("Updated board from Player 2:")
            tt.updateGameBoard(opponent_character, row, col)

            if not game_status(tt):
                game_active = False
                continue

        play_again = input("Would you like to play again? (Y/N): ")
        if play_again.lower() == 'n':
            conn.send("Fun Times".encode())
            tt.printStats()
            break
        elif play_again.lower() == 'y':
            conn.send("Play Again".encode())
            response = conn.recv(1024).decode()
            if response != "Play Again":
                print("Player 2 does not want to play again.")
                tt.printStats()
                break


def connection() -> None:
    """
    Establish a connection with Player 2 and start the game.

    Continuously prompt the user for host and port information until a successful connection is established.
    """
    # Prompt user for host info
    HOST = input("Enter the host name/IP address of Player 2: ")
    PORT = int(input("Enter the port for communication with Player 2: "))

    while True:
        try:
            # Open the socket
            p1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            p1_socket.connect((HOST, PORT))
            print('Successful Connection!')

            # Send Player 1's username
            player1 = input('Enter your username: ')
            p1_socket.sendall(player1.encode())

            # Receive data from player 2
            name_data = p1_socket.recv(1024).decode()
            print("Received User from Client:", name_data)

            # Play the game
            play_game(p1_socket, tt)

            # Close the connection
            p1_socket.close()
            break  # Exit loop after a successful game

        except Exception as e:
            print("Error:", e)
            retry = input('Enter "y" to retry and "n" to end the program: ')
            if retry != 'y':
                break

if __name__ == "__main__":
    connection()