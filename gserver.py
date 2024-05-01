import socket
import random

def generate_random_int(low, high):
    return random.randint(low, high)

def play_game(conn, guessme):
    conn.sendall(b"Enter your guess: ")
    tries = 0
    
    while True:
        client_input = conn.recv(1024)
        guess = int(client_input.decode().strip())
        tries += 1
        
        if guess == guessme:
            conn.sendall(b"Correct Answer!")
            return tries
        elif guess > guessme:
            conn.sendall(b"Guess Lower!\nEnter guess: ")
        elif guess < guessme:
            conn.sendall(b"Guess Higher!\nEnter guess: ")

def update_leaderboard(username, score):
    with open("leaderboard.txt", "a") as f:
        f.write(f"{username}: {score} tries\n")

def main():
    host = "192.168.1.5"
    port = 7777
    
    banner = "== Guessing Game v1.0 ==\n"
    difficulties = {'easy': (1, 50), 'medium': (1, 100), 'hard': (1, 500)}
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    
    print(f"Server is listening on port {port}")
    
    while True:
        conn, addr = s.accept()
        print(f"New client connected: {addr[0]}")
        
        guessme = 0
        username = ""
        score = 0
        
        while True:
            difficulty = conn.recv(1024).decode().strip().lower()
            if difficulty not in difficulties:
                conn.sendall(b"Invalid difficulty choice. Please choose again.")
                continue

            low, high = difficulties[difficulty]
            guessme = generate_random_int(low, high)

            tries = play_game(conn, guessme)

            if username:
                update_leaderboard(username, tries)

            conn.sendall(b"Do you want to play again? (yes/no): ")
            play_again = conn.recv(1024).decode().strip().lower()
            if play_again != 'yes':
                break
        leaderboard_text = "== Leaderboard ==\n"
        with open("leaderboard.txt", "r") as f:
            leaderboard_text += f.read()
        conn.sendall(leaderboard_text.encode())
        conn.close()

if __name__ == "__main__":
    main()
