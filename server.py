import socket
import threading

HOST = ''
PORT = 8001

def start_server():
    # Start the socket and wait for connections in another thread
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((HOST, PORT))
    server_socket.listen(2)

    print("Waiting for a connection. Server started")
    while True:
        conn, addr = server_socket.accept()
        print("Connected to:", addr)

        client_thread = threading.Thread(target=threaded_client(), args=(conn,))
        client_thread.start()

def threaded_client(self, conn):
    pass