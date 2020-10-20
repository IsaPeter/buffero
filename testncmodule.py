#!/usr/bin/env python3 
from subprocess import Popen 
from threading import Thread
import time



p = None
def donc():
    global p
    p = Popen("nc -lvnp 5050", shell=True) # something long running


t = Thread(target=donc)
t.start()
print("Launching TCP Reverse handler..")
time.sleep(2)
print("Sending Payload..")
print("Waiting for reverse shell..")
t.join()
time.sleep(5)
p.communicate()
