import socket
import sys
import os
import multiprocessing

def client_handler(conn, addr, q):
        while True:
            print(os.getpid() + '\n')
            msg_size = conn.recv(4)
            msg = conn.recv(int(msg_size))
            q.put(msg)
            q.task_done()

class Network:
    
    def close(self):
        if not (self.sock is None):
            self.sock.close()

    def host(self, port = 9090, max_client_queue = 10, pool_size = 10):
        self.sock = socket.socket()
        self.sock.bind(('', port))
        self.sock.listen(max_client_queue)
        
        ppool = multiprocessing.Pool(processes = pool_size)
        self.queue = multiprocessing.queues.JoinableQueue()

        while True:
            conn, addr = self.sock.accept()
            print('connected: ' + str(addr))
            #print(ppool.apply_async(os.getpid, ()).get(timeout = 1))
            ppool.apply_async(client_handler, (conn, addr, self.queue))
            print(self.queue.qsize())

    def connect(self, ip, port = 9090):
        self.sock = socket.socket()
        self.sock.connect((ip, port))

    def send(self, data, size):
        self.sock.send(str(size))
        self.sock.send(data)
    
    def __exit__(self):
        self.sock.close()

