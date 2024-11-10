import socket
from gameboard import BoardClass
#127.0.0.1
def game_status(tt: BoardClass, my_character: str) -> bool:
    """
    Check the game status to determine if there's a winner or if the board is full.

    Args:
        tt (BoardClass): The game board instance.
        my_character (str): The character of the current player ('x' or 'o').

    Returns:
        bool: True if the game should continue, False otherwise.
    """
    opponent = 'x' if my_character == 'o' else 'o'
    if tt.isWinner(my_character):
        if my_character == 'x':
            tt.x_wins += 1
            tt.o_loses += 1
            tt.turn = 'Player 1'
            print("Player 1 won!")
        else:
            tt.o_wins += 1
            tt.x_loses += 1
            tt.turn = 'Player 2'
            print("You won!")
        return False
    elif tt.isWinner(opponent):
        if opponent == 'x':
            tt.x_wins += 1
            tt.o_loses += 1
            tt.turn = 'Player 1'
            print("Player 1 won!")
        else:
            tt.o_wins += 1
            tt.x_loses += 1
            tt.turn = 'Player 2'
            print("You won!")
        return False
    if tt.boardIsFull():
        tt.ties += 1
        return False
    tt.username = 'Player 2'
    return True

def play_game(conn: socket.socket, tt: BoardClass) -> None:
    """
    Play the game of Tic-Tac-Toe between Player 1 and Player 2.

    Args:
        conn (socket.socket): The socket connection to the other player.
        tt (BoardClass): The game board instance.
    """
    my_character = 'o'
    opponent = 'x'
    numbers = [0, 1, 2]

    print('Instructions:')
    print('  1. You will use the numbers 0-2. 0 is the first row, 1 the second row, and 2 the third row. It is the same for columns.')
    print('  2. Your input should be structured like "0 1" with a space ONLY in between the numbers. Have Fun!')

    while True:
        tt.resetGameBoard()
        game_active = True
        tt.numofgames += 1

        while game_active:
            board_move_p1 = conn.recv(1024).decode()
            if not board_move_p1 or board_move_p1 == "Fun Times":
                print("Player 1 has left the game.")
                game_active = False
                break

            print("Player 1's move: ", board_move_p1)
            try:
                row, col = map(int, board_move_p1.split())
            except ValueError:
                print("Received invalid move from Player 1.")
                continue

            tt.updateGameBoard(opponent, row, col)

            if not game_status(tt, opponent):
                game_active = False
                break

            while True:
                my_move = input("Enter a row and column with a space in between (or 'q' to quit): ")
                if my_move.lower() == 'q':
                    conn.send("Fun Times".encode())
                    print("You quit the game.")
                    return

                try:
                    row, col = map(int, my_move.split())
                    if row not in numbers or col not in numbers:
                        print('Number is not valid, try again')
                        continue
                    elif tt.board[row][col] != 0:
                        print('Invalid move, try again')
                        continue
                    else:
                        tt.updateGameBoard(my_character, row, col)
                        conn.send(f"{row} {col}".encode())
                        break
                except ValueError:
                    print("Not a valid input. Try again")

            if not game_status(tt, my_character):
                game_active = False
                break

        play_again = input("Would you like to play again? (Y/N): ")
        if play_again.lower() == 'n':
            conn.send("Fun Times".encode())
            tt.printStats()
            break
        elif play_again.lower() == 'y':
            conn.send("Play Again".encode())
            response = conn.recv(1024).decode()
            if response != "Play Again":
                print("Player 1 does not want to play again.")
                tt.printStats()
                break


def connection() -> None:
    """
    Establish a connection with Player 1 and start the game.

    Continuously prompt the user for host and port information until a successful connection is established.
    """
    while True:
        try:
            # Prompt user for host info
            HOST = input("Enter the host name/IP address: ")

            # Prompt user for port info
            PORT = int(input("Enter the port for communication: "))

            # Open the socket
            p2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Establish connection
            p2_socket.bind((HOST, PORT))

            # Listen for incoming connections
            p2_socket.listen(5)

            # Accept the incoming connection
            conn, addr = p2_socket.accept()
            print("Successful Connection!")

            # Receive username from Player 1
            client_data = conn.recv(1024).decode()
            print("Received User from Client:", client_data)
            print('Waiting for player 1 to start...')

            # Send the username to Player 1
            player2 = 'Player 2'
            conn.sendall(player2.encode())

            # Initialize game board
            tt = BoardClass()

            # Play the game
            play_game(conn, tt)

            # Close the connection
            conn.close()
            p2_socket.close()
            break  # Exit loop after successful game

        except Exception as e:
            print("Error:", e)
            print("Try again")

if __name__ == "__main__":
    connection()