"""This module provides an asynchronous socket server.

It gets rid of the overhead of creating one thread per client,
and it limits the risk of race condition.

"""
import os
import time

import asyncore
import socket

BACKLOG = 5
SIZE = 1024

DEBUG = True

class Server(asyncore.dispatcher):

    allow_reuse_address         = False
    request_queue_size          = 5
    address_family              = socket.AF_INET
    socket_type                 = socket.SOCK_STREAM

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(self.address_family, self.socket_type)
        if self.allow_reuse_address:
            self.set_reuse_addr()
        self.bind((host, port))
        self.listen(self.request_queue_size)
        print "[!] Listening on port %s" % port

    # ------- Internal use -------
    def handle_accept(self):
        pair = self.accept()
        if pair:
            sock, addr = pair
            print "[!] conn_made: client_address=%s:%s" % (sock, addr)
            # print 'Incoming connection from %s' % repr(addr)
            ClientHandler(sock, addr)

class ClientHandler(asyncore.dispatcher_with_send):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server.

    Methods or channel events can be overriden to implement communication to the client.
    """
    def __init__(self, sock, address):
        # Create buffer holds data to write
        self.out_buffer = ""
        # We dont have anything to write, to start with
        self.is_writable = False
        # Store client address
        self.client_address = address

        asyncore.dispatcher.__init__(self, sock)

    def handle_read(self):
        """Called when the asynchronous loop detects that a read call on the channel's socket will succeed."""
        if DEBUG:
            data = self.recv(SIZE)
            if data:
                self.out_buffer += data
                print "**New Message** > %s" % data
            else:
                self.close()
        else:
            pass

    def handle_close(self):
        """Called when the socket is closed.

        There are two ways to detect whether a non-blocking socket is closed:

        select() returns a read event, but when you call recv()/read() you get zero bytes;
        call send()/write() and it fails with an error (sending zero bytes is not an error).

        Dispatcher will detect both low-level events and call this function.
        """
        print("conn_closed: client_address=%s:%s" % \
                     (self.client_address[0],
                      self.client_address[1]))
        self.close()


if __name__ == "__main__":

    HOST = socket.gethostbyname(socket.gethostname()) # socket.getfqdn()
    PORT = 9999

    s = Server(HOST, PORT)
    asyncore.loop() # does select() on dispatcher class, that wrappers around sockets.
