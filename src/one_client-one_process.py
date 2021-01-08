import socket, sys, time


def run_server(server_port=8080):
    server_sock = create_server(server_port)
    cid = 0
    while True:
        client_sock = accept_connect(server_sock, cid)
        serve_client(client_sock, cid)
        cid += 1


def create_server(server_port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    server_sock.bind(('127.0.0.1', server_port))
    server_sock.listen()
    return server_sock


def read_request(client_sock, delimiter=b'!'):
    request = bytearray()
    try:
        while True:
            chunk = client_sock.recv(4)
            if not chunk:
                print("Клиент преждевременно отключился")
                return None
            request += chunk
            if delimiter in request:
                return request
    except ConnectionError as e:
        print(f"Соединение было неожиданно разорвано: {e}")
        return None


def handle_request(request):
    time.sleep(5)
    return request[::-1]


def write_response(client_sock, response, cid):
    client_sock.sendall(response)
    client_sock.close()
    print(f"Запрос от клиента {cid} успешно обработан")


def serve_client(client_sock, cid):
    request = read_request(client_sock)
    if request is None:
        print(f"Клиент {cid} отключился")
    else:
        response = handle_request(request)
        write_response(client_sock, response, cid)


def accept_connect(server_sock, cid):
    client_sock, _ = server_sock.accept()
    print(f"Client: {cid} connected")
    return client_sock


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_server(int(sys.argv[1]))
    else:
        run_server()
