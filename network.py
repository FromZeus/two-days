import socket
import sys
import os
import multiprocessing
import threading
import time
import struct

def client_handler(conn, q):
    while True:
        print('in thread')
        msg_size_str = conn.recv(4)
        if not msg_size_str:
            return
        msg_size = struct.unpack('I', msg_size_str)[0]
        msg = conn.recv(msg_size)
        q.put(msg)
        #q.task_done()

class Network:
    
    def close(self):
        if not (self.sock is None):
            self.sock.close()

    def host(self, port = 9090, max_client_queue = 10):
        self.sock = socket.socket()
        self.sock.bind(('', port))
        self.sock.listen(max_client_queue)
        
        self.queue_dict = {}
        self.conn_dict = {}

        while True:
            conn, addr = self.sock.accept()
            self.conn_dict.update({addr: conn})
            print('connected: ' + str(addr))
            
            queue = multiprocessing.Queue()
            self.queue_dict.update({addr: queue})

            t = threading.Thread(target=client_handler, args=(conn, self.queue_dict[addr])
            t.start()

    def connect(self, ip, port = 9090):
        self.sock = socket.socket()
        self.sock.connect((ip, port))

    def send(self, data, size):
        msg_size = struct.pack('I', size)
        self.sock.send(msg_size)
        self.sock.send(data)
    
    def sendto(data, size, conn):
        msg_size = struct.pack('I', size)
        conn.send(msg_size)
        conn.send(data)

    def __exit__(self):
        self.sock.close()
