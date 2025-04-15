"""client"""
import socket
import threading
from rsa import generate_keys, encrypt_message, decrypt_message
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

        sent_private = decrypt_message(self.s.recv(1024).decode(), self.private_key).split(",")
        print(sent_private)
        print("-"*100)
        self.secret_key = tuple(sent_private)

        message_handler = threading.Thread(target=self.read_handler)
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler)
        input_handler.start()

    def read_handler(self):
        while True:
            message = self.s.recv(1024).decode()

            enc_message = decrypt_message(message, self.secret_key)

            print(enc_message)

    def write_handler(self):
        while True:
            message = input()
            self.s.send(encrypt_message(message, self.server_pub_key).encode())

if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, "b_g")
    cl.init_connection()
