import threading
import socket


def server():
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

                    print(f'[server] data: {data}, addr:{addr}')
                    con.sendall(f'Received: {data}'.encode())


def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 50007))
        s.sendall(b'client')
        data = s.recv(1024)
        print(f'[client] {data}')


def main():
    t1 = threading.Thread(target=server)
    t1.setDaemon(True)
    t1.start()

    t2 = threading.Thread(target=client)
    t2.setDaemon(True)
    t2.start()

    while True:
        s = input()
        if s == 'r':
            t2 = threading.Thread(target=client)
            t2.setDaemon(True)
            t2.start()
        elif s == 'q':
            break


if __name__ == "__main__":
    main()
