import socket
import threading
from rsa import generate_keys

class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.client_public_keys = {} 
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.public_key, self.private_key = generate_keys()

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)

        print(f"[server]: Сервер запущено на {self.host}:{self.port}")

        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print(f"{username} tries to connect")
            self.broadcast(f'{username} has joined the chat!')
            self.username_lookup[c] = username
            self.clients.append(c)

            c.send(f"{self.public_key[0]},{self.public_key[1]}".encode())

            client_pub_key = c.recv(1024).decode()
            e, n = map(int, client_pub_key.split(','))
            self.username_lookup[c] = {
                "username": username,
                "public_key": (e, n)
            }

            threading.Thread(target=self.handle_client, args=(c, addr)).start()

    def broadcast(self, msg: str):
        for client in self.clients:
            # тут шифрування і хешування
            client.send(msg.encode())

    def handle_client(self, c: socket, addr): 
        while True:
            msg = c.recv(1024)

            for client in self.clients:
                if client != c:
                    client.send(msg)

if __name__ == "__main__":
    s = Server(9001)
    s.start()