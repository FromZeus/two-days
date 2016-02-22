import network

nt1 = network.Network()
nt1.connect('localhost')

nt2 = network.Network()
nt2.connect('localhost')

nt1.send('nt1', 3)
nt1.send('nt1', 3)
nt2.send('nt2', 3)

nt1.close()
nt2.close()
