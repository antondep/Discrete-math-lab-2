"""server"""

import socket
import threading
from rsa import generate_keys, encrypt_message
import hashlib

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

        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            self.broadcast(f'{username} has joined the chat!')
            self.username_lookup[c] = username
            self.clients.append(c)

            public_e = self.public_key[0]
            public_n = self.public_key[1]
            public_key_str = f"{public_e},{public_n}"
            c.send(public_key_str.encode())

            client_pub_key = c.recv(1024).decode()
            parts = client_pub_key.split(',')
            e = int(parts[0])
            n = int(parts[1])

            private_key_str = f"{self.private_key[0]},{self.private_key[1]}"
            c.send(encrypt_message(private_key_str, (e, n)).encode())

            self.username_lookup[c] = {"username": username,"public_key": (e, n)}
            threading.Thread(target=self.handle_client, args=(c, addr)).start()

    def broadcast(self, msg: str):
        for client in self.clients:
            msg_hash = hashlib.sha256(msg.encode()).hexdigest()
            encrypted_msg = encrypt_message(f"{msg_hash}:,{msg}", self.public_key)
            client.send(encrypted_msg.encode())


    def handle_client(self, c: socket, addr):
        while True:
            msg = c.recv(1024).decode()

            for client in self.clients:
                if client != c:
                    client.send(msg.encode())

if __name__ == "__main__":
    s = Server(9001)
    s.start()
