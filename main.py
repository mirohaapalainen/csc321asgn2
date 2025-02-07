import os
import socket
import threading
import random
from hashlib import sha256
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

iv_global = get_random_bytes(AES.block_size)

class AESCipher:
    def __init__(self, key):
        self.cipher = None
        self.key = md5(key.encode('utf8')).digest()

    def encrypt(self, data):
        iv = iv_global
        self.cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(iv + self.cipher.encrypt(pad(data.encode('utf-8'),
                                                      AES.block_size)))

    def decrypt(self, data):
        raw = b64decode(data)
        self.cipher = AES.new(self.key, AES.MODE_CBC, raw[:AES.block_size])
        return unpad(self.cipher.decrypt(raw[AES.block_size:]), AES.block_size)


a = 27
q = 5
iv = os.urandom(16)


def power(a, x, q):
    if x == 1:
        return a
    return (a ** x) % q


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 9999))
    server_socket.listen(2)

    print("Server started, waiting for clients...")

    clients = []
    public_keys = []

    while len(clients) < 2:
        client_socket, addr = server_socket.accept()
        print(f"Client connected from {addr}")
        clients.append(client_socket)
        pub_key = int(client_socket.recv(1024).decode())
        public_keys.append(pub_key)

    # Exchange public keys
    clients[0].send(str(public_keys[1]).encode())
    clients[1].send(str(public_keys[0]).encode())

    # Close connections
    for c in clients:
        c.close()

    server_socket.close()


def client(name):
    private_key = random.randint(1, q - 1)
    public_key = power(a, private_key, q)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 9999))
    client_socket.send(str(public_key).encode())

    other_public_key = int(client_socket.recv(1024).decode())
    s = power(other_public_key, private_key, q)

    print(f"{name}: Shared Secret = {s}")

    k = sha256(str(s).encode('utf-8')).digest()

    print(f"{name}: SHA256-hashed secret: {k}")

    truncated_k = k[:16]

    print(f"{name}: Truncated SHA256-hashed secret: {k}")

    message = ""
    if name == "Alice":
        message = "Hi Bob!"
    else:
        message = "Hi Alice!"

    ciphertext = AESCipher(truncated_k).encrypt(message).decode('utf-8')

    client_socket.send(str(ciphertext).encode())
    other_message = str(client_socket.recv(1024).decode())

    client_socket.close()


# Run server in a separate thread
server_thread = threading.Thread(target=server, daemon=True)
server_thread.start()

# Run clients
threading.Thread(target=client, args=("Alice",)).start()
threading.Thread(target=client, args=("Bob",)).start()

while True:
    pass
