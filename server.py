import socket

class HttpRequest:
    def __init__(self, method, path, headers=None, body=None):
        self.method = method
        self.path = path
        self.headers = headers if headers is not None else {}
        self.body = body

def run_server():


    request1 = HttpRequest("GET", "/users")
    request2 = HttpRequest("GET", "/about")
    request3 = HttpRequest("POST", "/users", body='{"name": "Alex"}')

    print(f"Request 1: {request1.method} {request1.path}")
    print(f"Request 2: {request2.method} {request2.path}")
    print(f"Request 3: {request3.method} {request3.path}")
    print(f"Request 3 Body: {request3.body}")

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
            request_text   = request_bytes.decode('utf-8')
            lines = request_text.splitlines()
            if not lines:
                client_socket.close()
                continue

            first_line = lines[0]
            parts = first_line.split()
            path = "/"
            if len(parts) >= 2:
                method = parts[0]
                path = parts[1]
                print(f"Method: {method}")
                print(f"Path: {path}")

            headers = {}
            req_body = None
            body_parts = request_text.split('\r\n\r\n', 1)
            if len(body_parts) > 1:
                req_body = body_parts[1]

            for line in lines[1:]:
                if line == "":
                    break
                if ":" in line:
                    name, value = line.split(":", 1)
                    headers[name.strip()] = value.strip()




            if "Host" in headers:
                print(f"Host Header: {headers['Host']}")

            request = HttpRequest(
                method=method,
                path=path,
                headers=headers,
                body=req_body
            )

            print(f"Method: {request.method}")
            print(f"Path: {request.path}")
            print(f"Headers: {request.headers}")
            print(f"Body: {request.body}")

            if path == "/":
                resp_body = "Home Page"
            elif path == "/hello":
                resp_body = "Hello"
            elif path == "/about":
                resp_body = "About Page"
            else:
                resp_body = "404 Not Found"

            http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain; charset=utf-8\r\n"
                f'Content-Length: {len(resp_body)}\r\n'
                'Connection: close\r\n\r\n' + resp_body

            )
            client_socket.sendall(http_response.encode('utf-8'))
        client_socket.close()



if __name__ == '__main__':
    run_server()