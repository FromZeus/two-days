import socket
import sys
import os
import multiprocessing
import threading
import time
import struct
import zlib
import json


class Network:
    def client_handler(self, conn, q):
        while self.sv_status:
            msg_size_str = conn.recv(4)
            if not msg_size_str:
                break
            msg_size = struct.unpack('I', msg_size_str)[0]
            msg = conn.recv(msg_size)
            q.put(msg)
            #q.task_done()
        conn.close()

    def cl_disconnect(self):
        self.cl_status = 0

    def sv_disconnect(self):
        self.sv_status = 0
        self.cl_status = 0

    def host(self, port = 9090, max_client_queue = 10):
        self.sv_sock = socket.socket()
        self.sv_sock.bind(('', port))
        self.sv_sock.listen(max_client_queue)
        self.sv_status = 1
        
        self.queue_dict = {}
        self.conn_dict_sock = {}

        while self.sv_status:
            conn, addr = self.sv_sock.accept()
            self.conn_dict_sock.update({addr: conn})
            print('connected: ' + str(addr))
            
            queue = multiprocessing.Queue()
            self.queue_dict.update({addr: queue})

            t = threading.Thread(target=self.client_handler, args=(conn, self.queue_dict[addr]))
            t.start()
        self.sv_sock.close()

    def connect(self, ip, port = 9090):
        self.cl_sock = socket.socket()
        self.cl_sock.connect((ip, port))
        self.cl_status = 1
        self.cl_queue = multiprocessing.Queue()

        while self.cl_status:
            msg_size_str = self.cl_sock.recv(4)
            if not msg_size_str:
                break
            msg_size = struct.unpack('I', msg_size_str)[0]
            msg = self.cl_sock.recv(msg_size)
            self.cl_queue.put(msg)
        self.cl_sock.close()
    

    def cl_send(self, data):
        traffic = zlib.compress(json.dumps(data), 6)
        msg_size = struct.pack('I', len(traffic))
        self.cl_sock.send(msg_size)
        self.cl_sock.send(traffic)
    
    def sv_send(self, data, addr):
        traffic = zlib.compress(json.dumps(data), 6)
        msg_size = struct.pack('I', len(traffic))
        conn = self.conn_dict_sock[addr]
        conn.send(msg_size)
        conn.send(traffic)
        
    def __exit__(self):
        if self.cl_sock:
            self.cl_sock.close()
        if self.sv_sock:
            self.sv_sock.close()
            
