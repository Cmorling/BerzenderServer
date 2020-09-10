import socket
import commands
import db
import json
import argparse

def handleArgs():
    parser = argparse.ArgumentParser(description='Berzender server')
    parser.add_argument('-p', metavar='Port', type=int,
                    help='Port to host Berzender server')

    args = parser.parse_args()
    if not args.p:
        parser.print_help()
        exit()
    return {
        'port': args.p
    }

class Server():
    def __init__(self, host, port):
        self._host = host
        self._port = port

    def __enter__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self._host, self._port))
        sock.listen(10)
        self._sock = sock
        print('[*] Server running on {}'.format(self._port))
        return self._sock

    def __exit__(self, *exc_info):
        if exc_info[0]:
            import traceback
            traceback.print_exception(*exc_info)
        self._sock.close()

if __name__ == '__main__':
    host = 'localhost'
    a = handleArgs()
    with Server(host, a['port']) as s:
        with db.Database() as database:
            c = commands.Commands(database)
            while True:
                conn, addr = s.accept()
                msg = conn.recv(1024)
                try: 
                    payload = json.loads(msg.decode('utf-8'))
                    print('payload', payload)
                    response = c.handleCommand(payload)
                    print('response', response)
                    conn.send(json.dumps(response).encode())
                except:
                    pass
                finally:
                    conn.close()
