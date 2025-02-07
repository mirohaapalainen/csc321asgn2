import socket
import threading
import random


client_name = "NULL"


def generate_key(a, x, q):
    if x == 1:
        return a
    return (a ** x) % q


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\n<{client_name}> Received: {message}")
        except:
            break


def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))

    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    a = 5
    q = 37
    print(f"Generating random element from q = {q} and a = {a}...")
    x = random.randrange(0, q)
    key = generate_key(a, q)
    while True:
        print(f"Result: ")
        client_socket.send(message.encode('utf-8'))


client_name = input("Enter name for client:")
client()
