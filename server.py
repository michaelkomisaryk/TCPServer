import socket

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    HOST = 'localhost'
    PORT = 8080
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f'Server start working on {HOST}:{PORT} ')
    while True:
        client_socket, client_address = server_socket.accept()
        request_bytes = client_socket.recv(1024)
        if request_bytes:
            request_text = request_bytes.decode('utf-8')
            print(f'Revived HTTP request: {request_text}')

            body = 'Hello World'

            http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain; charset=utf-8\r\n"
                f'Content-Length: {len(body)}\r\n'
                'Connection: close\r\n\r\n' + body

            )
            client_socket.sendall(http_response.encode('utf-8'))
        client_socket.close()



if __name__ == '__main__':
    run_server()