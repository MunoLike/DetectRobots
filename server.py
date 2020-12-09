import socket


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('127.0.0.1', 50007))
    s.listen(1)

    while True:
        con, addr = s.accept()
        with con:
            while True:
                data = con.recv(1024)
                if not data:
                    break

                print(f'data: {data}, addr:{addr}')
                con.sendall(f'Received: {data}'.encode())
