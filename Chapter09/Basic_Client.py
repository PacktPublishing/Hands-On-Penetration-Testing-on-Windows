#!/usr/bin/python
import socket
webhost = '192.168.108.114'
webport = 80
print "Contacting %s on port %d ..." % (webhost, webport)
webclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
webclient.connect((webhost, webport))
webclient.send("GET / HTTP/1.1\r\nHost: 192.168.108.114\r\n\r\n")
reply = webclient.recv(4096)
print "Response from %s:" % webhost
print reply
