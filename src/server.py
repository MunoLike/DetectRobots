import socket


def server(lock):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 50007))
        s.listen(1)

        while True:
            con, addr = s.accept()
            with con:
                while True:
                    con.sendall(f'Received: {data}'.encode())
