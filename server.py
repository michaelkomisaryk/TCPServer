import socket

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = '127.0.0.1'
    PORT = 8080
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f'Server start working on {HOST}:{PORT} ')
    client_socket, client_address = server_socket.accept()
    print(f"Connected by {client_address}")
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    run_server()