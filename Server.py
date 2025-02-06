import socket
import threading


def handle_client(client_socket, other_client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Received: {message}")
            other_client_socket.send(message.encode())
        except:
            break


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 5555))
    server_socket.listen(2)
    print("Server listening on port 5555...")

    client1, _ = server_socket.accept()
    print("Client 1 connected.")

    client2, _ = server_socket.accept()
    print("Client 2 connected.")

    threading.Thread(target=handle_client, args=(client1, client2)).start()
    threading.Thread(target=handle_client, args=(client2, client1)).start()

server()