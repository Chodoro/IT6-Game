import socket

HOST = "localhost"
PORT = 7777

def main():
    s = socket.socket()
    s.connect((HOST, PORT))

    while True:
        data = s.recv(1024)
        print(data.decode().strip())

        difficulty = input("Enter difficulty: ")
        s.sendall(difficulty.encode())

        name = input("Enter your name: ")
        s.sendall(name.encode())

        while True:
            message = s.recv(1024)
            print(message.decode().strip())

            if "Leaderboard:" in message.decode():
                leaderboard_data = s.recv(1024)
                print(leaderboard_data.decode().strip())

            if "Correct" in message.decode():
                play_again = input("Would you like to play again? (yes/no): ")
                s.sendall(play_again.encode())

                if play_again.lower() == "no":
                    s.close()
                    return
                else:
                    break

            guess = input("Enter your guess: ")
            s.sendall(guess.encode())

    s.close()

if __name__ == "__main__":
    main()
