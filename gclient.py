import socket

def play_game(s, difficulty):
    s.sendall(difficulty.encode())
    
    while True:
        reply = s.recv(1024).decode().strip()
        print(reply)

        if "Correct" in reply:
            break

        user_input = input("").strip()
        s.sendall(user_input.encode())

def main():
    host = "192.168.1.5"
    port = 7777
    
    s = socket.socket()
    s.connect((host, port))
    
    data = s.recv(1024)
    print(data.decode().strip())
    
    while True:
        difficulty = input("Choose difficulty (easy/medium/hard): ").strip().lower()
        
        play_game(s, difficulty)
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            break
    
    s.close()

if __name__ == "__main__":
    main()
