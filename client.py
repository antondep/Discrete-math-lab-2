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
        parts = server_pub_key_raw.split(',')
        server_e = int(parts[0])
        server_n = int(parts[1])
        self.server_pub_key = (server_e, server_n)

        self.public_key, self.private_key = generate_keys()

        my_e = self.public_key[0]
        my_n = self.public_key[1]
        my_pub_key_str = f"{my_e},{my_n}"
        self.s.send(my_pub_key_str.encode())

        self.secret_key = None # add secret key

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
