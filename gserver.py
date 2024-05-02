import socket
import random
import json

HOST = "localhost"
PORT = 7777
LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file)

def generate_random_int(difficulty):
    if difficulty == "easy":
        return random.randint(1, 50)
    elif difficulty == "medium":
        return random.randint(1, 100)
    elif difficulty == "hard":
        return random.randint(1, 500)
    else:
        return random.randint(1, 100)

def play_game(conn):
    conn.sendall(b"Welcome to the Guessing Game! Select difficulty: (easy/medium/hard)")
    difficulty = conn.recv(1024).decode().strip()
    number_to_guess = generate_random_int(difficulty)
    tries = 0

    conn.sendall(b"Make a guess: ")
    name = conn.recv(1024).decode().strip()

    while True:
        guess = int(conn.recv(1024).decode().strip())
        tries += 1

        if guess == number_to_guess:
            leaderboard = load_leaderboard()
            if name in leaderboard:
                if tries < leaderboard[name]:
                    leaderboard[name] = tries
            else:
                leaderboard[name] = tries

            save_leaderboard(leaderboard)

            conn.sendall(b"Correct Answer! Would you like to play again? (yes/no): ")
            play_again = conn.recv(1024).decode().strip()
            if play_again.lower() == "no":
                conn.close()
                return
            else:
                play_game(conn)
                break

        elif guess < number_to_guess:
            conn.sendall(b"Guess Higher!")
        else:
            conn.sendall(b"Guess Lower!")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Server is listening on port {PORT}")

    while True:
        conn, addr = s.accept()
        print(f"New client connected: {addr}")
        play_game(conn)

    s.close()

if __name__ == "__main__":
    main()
