import socket
import random

HOST = "localhost"
PORT = 7777
LEADERBOARD_FILE = "leaderboard.txt"

def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as file:
        file.writelines(leaderboard)

def generate_random_int(difficulty):
    if difficulty == "easy":
        return random.randint(1, 50)
    elif difficulty == "medium":
        return random.randint(1, 100)
    elif difficulty == "hard":
        return random.randint(1, 500)
    else:
        return random.randint(1, 100)

def update_leaderboard(name, attempts, difficulty):
    leaderboard = load_leaderboard()
    updated_leaderboard = []

    updated_entry = f"{name} attempts - {attempts} {difficulty}\n"
    inserted = False

    for line in leaderboard:
        if not inserted and "TOP" not in line:
            old_attempts = int(line.split('-')[1].split()[0])
            if attempts < old_attempts:
                updated_leaderboard.append(updated_entry)
                inserted = True
        updated_leaderboard.append(line)
    
    if not inserted:
        updated_leaderboard.append(updated_entry)

    updated_leaderboard.sort(key=lambda x: int(x.split('-')[1].split()[0]))

    save_leaderboard(updated_leaderboard)

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
            update_leaderboard(name, tries, difficulty)

            leaderboard = load_leaderboard()
            conn.sendall(b"Correct Answer!\nLeaderboard:\n" + ''.join(leaderboard).encode())
            
            conn.sendall(b"Would you like to play again? (yes/no): ")
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
