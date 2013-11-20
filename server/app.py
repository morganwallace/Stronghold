#!/usr/bin/python
import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from wsgiref.handlers import CGIHandler
import flask
from flask import Flask
from flask import render_template
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    def inner():
        for x in range(100):
            # time.sleep(0.1)
            yield '%s<br/>\n' % x
    env = Environment(loader=FileSystemLoader('templates'))
    tmpl = env.get_template('index.html')
    # result=
    return flask.Response(tmpl.generate(result=inner()))
    # return render_template('index.html',result)
    # return "Hello world"




# def data_gen():
#     t = data_gen.t
#     cnt = 0
#     while cnt < 1000: # limit the time to 50 secs
#         cnt+=1
#         t += 0.05
#         y=get_data_from_serial()
#         print y
#         if y!= None: 
#             yield t, y
#     # else: yield data_gen()
# data_gen.t = 0

# fig, ax = plt.subplots()
# line, = ax.plot([], [], lw=2)
# ax.set_ylim(-1.1, 1.1)
# ax.set_xlim(0, 5)
# ax.grid()
# xdata, ydata = [], []
# def run(data):
#     # update the data
#     t,y = data
#     xdata.append(t)
#     ydata.append(y)
#     xmin, xmax = ax.get_xlim()

#     if t >= xmax:
#         ax.set_xlim(xmin, 2*xmax)
#         ax.figure.canvas.draw()
#     line.set_data(xdata, ydata)

#     return line,

# ser = serial.Serial('/dev/tty.usbmodem1421', 9600)
# def get_data_from_serial():
#     s=ser.readline()
#     print s
#     s=s.split(",")
#     if len(s)!=3:
#         return None
#     for i in range(len(s)):
#         try:s[i]=float(s[i].strip())
#         except: return None
#     # print s
#     xg, xy, xz = s[0],s[1],s[2]
#     return xy

# ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=10,
#     repeat=False)
# plt.show()


if __name__ == '__main__':
    app.run(port=7000)