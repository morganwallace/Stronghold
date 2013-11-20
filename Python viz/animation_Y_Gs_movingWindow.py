from __future__ import division
import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def data_gen():
    t = data_gen.t
    cnt = 0
    while cnt < 2000: # limit the time to 50 secs
        cnt+=1
        t += 0.05
        y=get_data_from_serial()
        print y
        if y!= None: 
            yield t, y
    # else: yield data_gen()
data_gen.t = 0

fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_ylim(-3.1, 1.1)
ax.set_xlim(0, 10)
ax.grid()
xdata, ydata = [], []
def run(data):
    # update the data
    t,y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()

    if t >= xmax-1: #once the line get's halfway...
        #move the window by 1/20th of a second forward
        xmin+=5
        xmax+=5 
        ax.set_xlim(xmin, xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,

ser = serial.Serial('/dev/tty.usbmodem1421', 9600)
def get_data_from_serial():
    s=ser.readline()
    print s
    s=s.split(",")
    if len(s)!=3:
        return None
    for i in range(len(s)):
        try:s[i]=float(s[i].strip())
        except: return None
    # print s
    xg, xy, xz = s[0],s[1],s[2]
    return xz

ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=10,
    repeat=False)
plt.show()
