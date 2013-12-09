from __future__ import division
import serial
import time
import os
import pickle
import animation_debug
import matplotlib.pyplot as plt
# import matplotlib
import matplotlib.animation as animation
'''
#################################################

1. Process the buffer in the Serial port from the
accelerometer to find peaks.

2. Send peak data (timing) to another Serial port
so that Processing can read it in real-time
#################################################
'''
data=[]
slopes=[]
start_time=time.time()
######  Preferences Variables  ######
sampleRate=.2 #this is set by the code on Arduino
max_rep_window=5 #seconds
min_rep_window=.4 #seconds
initialize_time=1 #second

player=2

#Attempt serial connection
try:
    ser = serial.Serial('/dev/tty.usbmodem1411', 9600)

#Failed serial connections used old test data
except:
    print "no serial activity; reverting to test data"
    ser=pickle.load(open("curls_test2.p","rb"))

#output files reset to 0
with open("player"+str(player)+"repair.txt" ,'w+') as out_file:
    # out_file.seek(0)
    out_file.write("0")
with open("player"+str(player)+"shoot.txt" ,'w+') as out_file:
    # out_file.seek(0)
    out_file.write("0")


def get_data_from_serial():
    global ser
    try:
        serialOutput=ser.readline()
    except:#in case you don't have usb and are going off of old data
        time.sleep(.2)
        try:serialOutput=ser[0]
        except:quit()
        del ser[0]
        return serialOutput
    # quit()
    print serialOutput
    serialTuple=serialOutput.split(",")
    if len(serialTuple)!=3:
        return None
    for i in range(len(serialTuple)):
        try:serialTuple[i]=float(serialTuple[i].strip())
        except: return None
    x, y, z = serialTuple[0],serialTuple[1],serialTuple[2]
    t=time.time()
    return t,x,y,z


def get_slope(axis,datalist, samples=2):
    rise=datalist[-1][axis] - datalist[-samples][axis] #acc value, for x, i=1;    y, i=2;    z, i=3
    run=datalist[-1][0] - datalist[-samples][0] #time change
    return rise/run

def rep_event(exer, root_times=(0,0)):
    global data
    global player
    del(data[:-1])

    #record reps by player and also by event
    if exer==3:
        
        with open("player"+str(player)+"shoot.txt" ,'r+') as out_file:
            file_reps=int(out_file.read())+1
            print "Player"+str(player)+" shooting:" + "reps: "+str(file_reps)
            out_file.seek(0)
            out_file.write(str(file_reps))

    elif exer !=3:
        with open("player"+str(player)+"repair.txt" ,'r+') as out_file:
            file_reps=int(out_file.read())+1
            print "Player"+str(player)+" repair:" + "reps: "+str(file_reps)
            out_file.seek(0)
            out_file.write(str(file_reps))


peak_x,peak_y,peak_z,dip_x,dip_y,dip_z=0,0,0,0,0,0
def detect_rep():
    global data,peak_x,peak_y,peak_z,dip_x,dip_y,dip_z
    #only look for reps after the min rep window
    # min_samples=int(min_rep_window/sampleRate)
    # if len(data)>=min_samples:

    #find max and min for each axis - !must be a more effiecient way!
    # for axis in (3,2,1):
        #isolate data for axis
        # values=[sample[axis] for sample in data]

    # if len(data)<min_samples
    #     peak=max(values)
    #     dip=min(values)

    #More efficient but complicated way
    # print data
    if len(data)<2:
        peak_x,peak_y,peak_z,dip_x,dip_y,dip_z,range_x,range_y,range_z=0,0,0,0,0,0,0,0,0
        print 'test'
    else:
        # print peak_x
        sample=data[-1]
        # print sample
        # peaks
        if sample[1]>peak_x:  
            peak_x=sample[1]
            range_x=peak_x - dip_x
        if sample[2]>peak_y:  
            peak_y=sample[2]
            range_y=peak_y - dip_y
        if sample[3]>peak_z:  
            peak_z=sample[3]
            range_z=peak_z - dip_z
        # dips
        if sample[1]<dip_x:  
            dip_x=sample[1]
            range_x=peak_x - dip_x
        if sample[2]<dip_y:  
            dip_y=sample[2]
            range_y=peak_y - dip_y
        if sample[3]<dip_z:  
            dip_z=sample[3]
            range_z=peak_z - dip_z
        # print "%d, %d, %d" % (range_x,range_y,range_z)

        # last-half of cycle
        # defined by latest datum not being max or min and
        # if the up or down motion caused at least .4 g
        axis=3
        if (peak_z-dip_z>.6) and (dip_z< data[-1][3] < peak_z):
            #print axis
            exercise = axis

            #direction of slope can tell you what to expect
            if get_slope(axis, data) > 0:
                curve="valley"
            else:
                curve ="hill"
            # print curve

            #get the time for this point - halfway through the rep
            halftime=time.time()

            #wait and look for return to starting point
            while time.time()-halftime<=max_rep_window/2:
                data.append(get_data_from_serial())
                if curve == "valley":
                    if data[-1][axis] >=peak_z-.2:
                        rep_event(exercise)
                        peak_z=0
                        dip_z=0
                        break
                elif curve == "hill":
                    if data[-1][axis] <=dip_z+.2:
                        rep_event(exercise)
                        peak_z=0
                        dip=0
                        break

def data_gen():
    global data
    yield data[-1]
#modifiable variables
runningTime=15 #seconds
exerciseType="test"
movingWindow=True
sampleRate =0.2 # set in arduino code!!
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
ax.set_ylim(-1.5, 1.5)
ax.set_xlim(0, runningTime)

if movingWindow==True: ax.set_xlim(0, 20)
ax.grid()
ax.set_xlabel('time (s)')
ax.set_ylabel('acceleration (g)')
ax.set_title(exerciseType)

def run(D):
    # print D
    # update the data
    global movingWindow
    t,x,y,z = data_gen()
    tdata.append(t)
    ydata.append(y)
    xdata.append(x)
    zdata.append(z)
    print tdata
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

def main():
    global data
    global sampleRate
    global max_rep_window
    global min_rep_window
    global start_time

    #loops forever
    while True:
        #limit time for rep detection to 5 seconds
        if len(data)*sampleRate>=max_rep_window: 
            del data[0]
            
        #Get time, x, y, and z from serial port
        data.append(get_data_from_serial())

        if data:
            detect_rep()

        ani = animation.FuncAnimation(fig, run, blit=False, interval=10,repeat=True)
        plt.show()
        
        

if __name__ == '__main__':
    main()
    animation_debug.animate(data_gen)
