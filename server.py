import socket
import json


users = []


class HttpRequest:
    def __init__(self, method, path, headers=None, body=None):
        self.method = method
        self.path = path
        self.headers = headers if headers is not None else {}
        self.body = body

    def print_info(self):
        print(f"Method: {self.method}")
        print(f"Path: {self.path}")
        print(f"Headers: {self.headers}")
        print(f"Body: {self.body}")


class HttpResponse:
    def __init__(self, status_code, headers=None, body=""):
        self.status_code = status_code
        self.headers = headers if headers is not None else {}
        self.body = body

    def to_http_text(self):
        status_messages = {
            200: "OK",
            201: "Created",
            400: "Bad Request",
            404: "Not Found"
        }

        status_message = status_messages.get(self.status_code, "")

        self.headers["Content-Length"] = str(
            len(self.body.encode("utf-8"))
        )

        response_text = (
            f"HTTP/1.1 {self.status_code} {status_message}\r\n"
        )

        for name, value in self.headers.items():
            response_text += f"{name}: {value}\r\n"

        response_text += "\r\n"
        response_text += self.body

        return response_text


def home_handler(request):
    return HttpResponse(
        status_code=200,
        headers={"Content-Type": "text/plain; charset=utf-8"},
        body="Home Page"
    )


def hello_handler(request):
    return HttpResponse(
        status_code=200,
        headers={"Content-Type": "text/plain; charset=utf-8"},
        body="Hello"
    )


def about_handler(request):
    return HttpResponse(
        status_code=200,
        headers={"Content-Type": "text/plain; charset=utf-8"},
        body="About Page"
    )


def api_info_handler(request):
    data = {
        "name": "My Python Server",
        "version": "1.0"
    }

    return HttpResponse(
        status_code=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(data)
    )


def users_handler(request):
    data = json.loads(request.body)

    if "name" not in data:
        return HttpResponse(
            status_code=400,
            headers={"Content-Type": "application/json"},
            body=json.dumps({
                "error": "Name is required"
            })
        )

    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "age": data.get("age")
    }

    users.append(new_user)

    print(f"Created user: {new_user}")
    print(f"Users: {users}")

    return HttpResponse(
        status_code=201,
        headers={"Content-Type": "application/json"},
        body=json.dumps(new_user)
    )


def get_users_handler(request):
    return HttpResponse(
        status_code=200,
        headers={"Content-Type": "application/json"},
        body=json.dumps(users)
    )


def get_user_handler(request):
    user_id = int(request.path.split("/")[-1])

    for user in users:
        if user["id"] == user_id:
            return HttpResponse(
                status_code=200,
                headers={"Content-Type": "application/json"},
                body=json.dumps(user)
            )

    return HttpResponse(
        status_code=404,
        headers={"Content-Type": "application/json"},
        body=json.dumps({
            "error": "User not found"
        })
    )


def update_user_handler(request):
    user_id = int(request.path.split("/")[-1])

    for user in users:
        if user["id"] == user_id:
            data = json.loads(request.body)

            user["name"] = data["name"]
            user["age"] = data["age"]

            return HttpResponse(
                status_code=200,
                headers={"Content-Type": "application/json"},
                body=json.dumps(user)
            )

    return HttpResponse(
        status_code=404,
        headers={"Content-Type": "application/json"},
        body=json.dumps({
            "error": "User not found"
        })
    )


def delete_user_handler(request):
    user_id = int(request.path.split("/")[-1])

    for user in users:
        if user["id"] == user_id:
            users.remove(user)

            return HttpResponse(
                status_code=200,
                headers={"Content-Type": "application/json"},
                body=json.dumps({
                    "message": "User deleted"
                })
            )

    return HttpResponse(
        status_code=404,
        headers={"Content-Type": "application/json"},
        body=json.dumps({
            "error": "User not found"
        })
    )


class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, method, path, handler):
        self.routes[(method, path)] = handler

    def find_route(self, method, path):
        if method == "GET" and path.startswith("/users/"):
            return get_user_handler

        if method == "PUT" and path.startswith("/users/"):
            return update_user_handler

        if method == "DELETE" and path.startswith("/users/"):
            return delete_user_handler

        return self.routes.get((method, path))

    def handle(self, request):
        handler = self.find_route(
            request.method,
            request.path
        )

        if handler is None:
            return HttpResponse(
                status_code=404,
                headers={"Content-Type": "text/plain; charset=utf-8"},
                body="404 Not Found"
            )

        return handler(request)


def run_server():
    router = Router()

    router.add_route("GET", "/", home_handler)
    router.add_route("GET", "/hello", hello_handler)
    router.add_route("GET", "/about", about_handler)
    router.add_route("GET", "/api/info", api_info_handler)
    router.add_route("POST", "/users", users_handler)
    router.add_route("GET", "/users", get_users_handler)

    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    HOST = "localhost"
    PORT = 8080

    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"Server started on http://{HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()

        request_bytes = b""

        while b"\r\n\r\n" not in request_bytes:
            chunk = client_socket.recv(1024)

            if not chunk:
                break

            request_bytes += chunk

        if not request_bytes:
            client_socket.close()
            continue

        header_bytes, _, body_bytes = request_bytes.partition(
            b"\r\n\r\n"
        )

        header_text = header_bytes.decode("utf-8")
        lines = header_text.split("\r\n")

        first_line = lines[0]
        parts = first_line.split()

        if len(parts) < 2:
            client_socket.close()
            continue

        method = parts[0]
        path = parts[1]

        headers = {}

        for line in lines[1:]:
            if ":" in line:
                name, value = line.split(":", 1)
                headers[name.strip()] = value.strip()

        content_length = int(
            headers.get("Content-Length", 0)
        )

        while len(body_bytes) < content_length:
            chunk = client_socket.recv(
                content_length - len(body_bytes)
            )

            if not chunk:
                break

            body_bytes += chunk

        body = body_bytes.decode("utf-8")

        request = HttpRequest(
            method=method,
            path=path,
            headers=headers,
            body=body
        )

        request.print_info()

        response = router.handle(request)

        http_text = response.to_http_text()

        client_socket.sendall(
            http_text.encode("utf-8")
        )

        client_socket.close()


if __name__ == "__main__":
    run_server()