import socket
import threading

class GameClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            print("Connected to server")

            receive_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
            receive_thread.start()

            while True:
                city = input("Enter a city: ")
                client_socket.sendall(city.encode())

    def receive_messages(self, client_socket):
        while True:
            message = client_socket.recv(1024).decode()
            if message:
                print(message)

if __name__ == "__main__":
    client = GameClient()
    client.start()
