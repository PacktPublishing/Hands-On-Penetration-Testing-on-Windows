#!/usr/bin/python
from scapy.all import *
CPIPADDRESS="192.168.108.215"
SOURCEP=random.randint(1024,65535)
ip=IP(dst=CPIPADDRESS, flags="DF", ttl=64)
tcpopt=[("MSS",1460), ("NOP",None), ("WScale",2), ("NOP",None), ("NOP",None), ("Timestamp",(123,0)), ("SAckOK",""), ("EOL",None)]
SYN=TCP(sport=SOURCEP, dport=80, flags="S", seq=1000, window=0xffff, options=tcpopt)
SYNACK=sr1(ip/SYN)
ACK=TCP(sport=SOURCEP, dport=80, flags="A", seq=SYNACK.ack+1, ack=SYNACK.seq+1, window=0xffff)
send(ip/ACK)
request="GET / HTTP/1.1\r\nHost: " + CPIPADDRESS + "\rMozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1 \r\n\r\n"
PUSH=TCP(sport=SOURCEP, dport=80, flags="PA", seq=1001, ack=0, window=0xffff)
send(ip/PUSH/request)
RST=TCP(sport=SOURCEP, dport=80, flags="R", seq=1001, ack=0, window=0xffff)
send(ip/RST)
