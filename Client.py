import socket
import threading
import random


client_name = "NULL"
a_global = 5
q_global = 37
x = random.randrange(0, q_global)


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

    while True:
        message = input("Enter message: ")
        client_socket.send(message.encode('utf-8'))


client_name = input("Enter name for client:")
client()
