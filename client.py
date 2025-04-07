import socket
import threading
from rsa import generate_keys
class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        self.s.send(self.username.encode())

        server_pub_key_raw = self.s.recv(1024).decode()
        e, n = map(int, server_pub_key_raw.split(','))
        self.server_pub_key = (e, n)

        self.public_key, self.private_key = generate_keys()

        self.s.send(f"{self.public_key[0]},{self.public_key[1]}".encode())

        self.secret_key = None # add a secret key

        message_handler = threading.Thread(target=self.read_handler)
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler)
        input_handler.start()

    def read_handler(self):
        while True:
            message = self.s.recv(1024).decode()

            # decrypt message with the secrete key

            # ... 


            print(message)

    def write_handler(self):
        while True:
            message = input()

            # encrypt message with the secrete key

            # ...

            self.s.send(message.encode())

if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, "b_g")
    cl.init_connection()
