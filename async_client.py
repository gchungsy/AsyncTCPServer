import asyncore
import socket

class Client(asyncore.dispatcher_with_send):
    def __init__(self, host, port, message):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.out_buffer = message

    def handle_close(self):
        self.close()

    def handle_read(self):
        print " ClientA received data:", self.recv(1024)
        self.out_buffer = raw_input("tcpClientA: Enter message to continue: ")

def ClientA():
    # Python TCP Client B - Async
    msg = raw_input("tcpClientA: Enter message to continue: ")
    c = Client(socket.gethostname(), 9999, msg)
    asyncore.loop()


def ClientB():
    # Python TCP Client B - not Async
    host = socket.gethostname()
    port = 9999
    BUFFER_SIZE = 1024
    MESSAGE = raw_input("tcpClientB: Enter message: ")

    tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpClientA.connect((host, port))

    while MESSAGE != 'exit':
        tcpClientA.send(MESSAGE)
        data = tcpClientA.recv(BUFFER_SIZE)
        print " ClientB received data:", data
        MESSAGE = raw_input("tcpClientB: Enter message to continue: ")

    tcpClientA.close()

if __name__ == '__main__':
    ClientA()
    ClientB()
