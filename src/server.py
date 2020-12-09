import socket
import logging
import main

# logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def server(lock):
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

                    logger.info(f'connect from: {addr}')

                    coords = None
                    lock.acquire()
                    coords = main.get_coords()
                    lock.release()

                    sendstr = f'{coords[0][0]},{coords[0][1]},{coords[1][0]},{coords[1][1]}'

                    con.sendall(sendstr.encode())

                    logger.info(f'send pos{coords}')
