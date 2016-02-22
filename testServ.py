import network
import threading
import time
def print_dict(nt):
    for i in range(3):
        time.sleep(4)
        print(nt.queue_dict)


nt = network.Network()
t = threading.Thread(target=print_dict, args=(nt, ))
nt.host()



#while True:
#    print(nt.queue.get())
    #print(nt.queue.get())
