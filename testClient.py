import network

nt1 = network.Network()
nt1.connect('localhost')

nt2 = network.Network()
nt2.connect('localhost')

nt1.send({'nt1': 4})
nt1.send({'nt1': 4})
nt2.send({'nt2': 2})

nt1.cl_disconnect()
nt2.cl_disconnect()
