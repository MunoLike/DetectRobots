import socket
import logging
import variables

# logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def server(lock):
    def f(e): return '{:.3g}'.format(e)

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
                    coords = variables.coords
                    lock.release()

                    redp = list(map(f, variables.coords[0]))
                    bluep = list(map(f, variables.coords[1]))
                    sendstr = f'{redp[0]},{redp[1]},{bluep[0]},{bluep[1]}'

                    con.sendall(sendstr.encode())

                    logger.info(f'send pos{coords}')
