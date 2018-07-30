#!/usr/bin/python
import socket
import threading
host_ip = '0.0.0.0'
host_port = 45678
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host_ip, host_port))
server.listen(4)
print "Server is up. Listening on %s:%d" % (host_ip, host_port)
def connect(client_socket):
    received = client_socket.recv(1024)
    print "Received from remote client:\n-----------\n%s\n-----------\n" % received
    client_socket.send("Always listening, comrade!\n\r")
    print "Comrade message sent. Closing connection."
    client_socket.close()
    print "\nListening on %s:%d\n" % (host_ip, host_port)
while True:
    client, address = server.accept()
    print "Connection accepted from remote host %s:%d" % (address[0], address[1])
    client_handler = threading.Thread(target=connect, args=(client,))
    client_handler.start()
