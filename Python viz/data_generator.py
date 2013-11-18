import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def data_gen():
    t = data_gen.t
    cnt = 0
    while cnt < 1000:
        cnt+=1
        t += 0.05
        y=get_data_from_serial()
        if y!= None: yield t, y
data_gen.t = 0


ser = serial.Serial('/dev/tty.usbmodem1421', 9600)
def get_data_from_serial():
    s=ser.readline()
    print s
    s=s.split(",")
    if len(s)!=3:
        return None
    for i in range(len(s)):
        try: s[i]=float(s[i].strip())
        except: return None
    print s
    xg, xy, xz = s[0],s[1],s[2]
    return xy

# while True:
#     print serial.Serial('/dev/tty.usbmodem1421', 9600).readline()

while True:
    l=data_gen()
    for i in l:
        print i
