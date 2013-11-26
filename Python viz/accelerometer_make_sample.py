from __future__ import division
import serial
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.animation as animation
import pickle
import os
import csv



#modifiable variables
runningTime=50 #seconds
exerciseType="lateral_raise"
movingWindow=False

#Make OS appropriate output filename
# now =time.asctime()[4:-5]
now = time.strftime("%Y-%m-%d__%H:%M:%S")
dirname="labeled_data/"+now+"_"+exerciseType
filename=now+"_"+exerciseType

#Initialized variables
samples=[]



fig,ax = plt.subplots()

# fig = matplotlib..figure.Figure(figsize=(8,6))
tdata, xdata, ydata, zdata = [], [],[],[]

    #Vizualization parameters
lineX, = ax.plot([], [],"r-", lw=2,label="X")
lineY, = ax.plot([], [],"g-", lw=2,label="Y")
lineZ, = ax.plot([], [],"b-", lw=2,label="Z")
legend=plt.legend()
ax.set_ylim(-2.0, 2.0)
ax.set_xlim(0, runningTime)
ax.grid()
ax.set_xlabel('time (s)')
ax.set_ylabel('acceleration (g)')



def data_gen():
    '''Generator that yields data for real-time animation
    Get's data from the
    '''
    global runningTime
    global samples

    sampleRate =0.05
    t = data_gen.t
    timePassed = 0

    # limit the time to runningTime
    while timePassed < runningTime: 
        timePassed+=.05
        t += sampleRate
        try:
            x,y,z=get_data_from_serial()
        except:
            x,y,z =0,0,0
        if y!= None: 
            data =t,x,y,z 
            samples.append(data)
            yield data
    #save to file for later analysis.
    ser.close()
    save(samples)
    print "done"
    
data_gen.t = 0

def save(samples):
    '''Save csv and png of sampled data
    '''
    global dirname
    global filename
    os.mkdir(dirname)
    picpath=dirname+"/test.png"
    plt.savefig(picpath)
    pickle.dump(samples,open(dirname+"/"+filename+".p","wb"))
    with open(dirname+"/"+filename+".csv","wb") as csvFile:
        writer=csv.writer(csvFile)
        writer.writerow(["t (sec)","x","y","z"]) #header
        for i in samples:
            writer.writerow((i))



def run(data):
    # update the data
    global movingWindow
    t,x,y,z = data
    tdata.append(t)
    ydata.append(y)
    xdata.append(x)
    zdata.append(z)
    xmin, xmax = ax.get_xlim()
    if movingWindow==True:
        if t >= xmax-1: #once the line get's halfway...
            #move the window by 1/20th of a second forward
            xmin+=5
            xmax+=5 
            ax.set_xlim(xmin, xmax)
            ax.figure.canvas.draw()
    lineX.set_data(tdata, xdata)
    lineY.set_data(tdata, ydata)
    lineZ.set_data(tdata, zdata)
    return lineX,lineY,lineZ

ser = serial.Serial('/dev/tty.usbmodem1421', 9600)
def get_data_from_serial():
    serialOutput=ser.readline()
    print serialOutput
    s=serialOutput.split(",")
    if len(s)!=3:
        return None
    for i in range(len(s)):
        try:s[i]=float(s[i].strip())
        except: return None
    # print s
    x, y, z = s[0],s[1],s[2]
    return x,y,z

ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=10,
    repeat=False)
plt.show()

