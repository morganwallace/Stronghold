from __future__ import division
import serial
import time
import os
import pickle

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
    # print serialOutput
    serialTuple=serialOutput.split(",")
    if len(serialTuple)!=3:
        return None
    for i in range(len(serialTuple)):
        try:serialTuple[i]=float(serialTuple[i].strip())
        except: return None
    x, y, z = serialTuple[0],serialTuple[1],serialTuple[2]
    t=time.time()
    return t,x,y,z


def get_slope(axis, samples=2):
    """returns the slope of the axis from the 
    second to last point to the current point"""
    global data
    rise=data[-1][axis] - data[-samples][axis] #acc value, for x, i=1;    y, i=2;    z, i=3
    run=data[-1][0] - data[-samples][0] #time change
    return rise/run

def rep_event(exer, root_times=(0,0)):
    """This is triggered when we have detected a rep.
    This function increments the rep count which is saved
    in a file accessible to our game running in Processing"""
    global data
    global player
    del(data[:-1])

    #record reps by player and also by exercise type (curl or lateral raise)
    if exer=="latRaise":
        with open("player"+str(player)+"shoot.txt" ,'r+') as out_file:
            file_reps=int(out_file.read())+1
            print "Player"+str(player)+" shooting:" + "reps: "+str(file_reps)
            out_file.seek(0)
            out_file.write(str(file_reps))

    elif exer =="curl":
        with open("player"+str(player)+"repair.txt" ,'r+') as out_file:
            file_reps=int(out_file.read())+1
            print "Player"+str(player)+" repair:" + "reps: "+str(file_reps)
            out_file.seek(0)
            out_file.write(str(file_reps))


def halfway(axis,peak,dip):
    print "in halfway"
    global data
    global max_rep_window
    # print axis
    # print "%f, %f (peak,dip)" %(peak,dip)
    #direction of slope can tell you what to expect
    if get_slope(axis) > 0:
        curve="valley"
    else:
        curve ="hill"
    # print curve

    #get the time for this point - halfway through the rep
    halftime=time.time()
    # print str(peak-dip)
    if peak-dip>1.15:
        exercise="curl"
    else:
        exercise="latRaise"
    #wait and look for return to starting point
    while time.time()-halftime<=max_rep_window/2:
        data.append(get_data_from_serial())
        if curve == "valley":
            if data[-1][axis] >=peak-.3 and get_slope(axis)<=0:
                rep_event(exercise)
                break
        elif curve == "hill":
            if data[-1][axis] <=dip+.3 and get_slope(axis)>=0:
                rep_event(exercise)
                break
        # time.sleep(.2)

peaks=-0
prev_y_slope=0
peak_x,peak_y,peak_z,dip_x,dip_y,dip_z,range_x,range_y,range_z=0,0,0,0,0,0,0,0,0
def detect_rep():
    global data,peak_x,peak_y,peak_z,dip_x,dip_y,dip_z,range_x,range_y,range_z
    global prev_y_slope
    global peaks
    # print data
    #data  looks like [(.2,,5,-1.1,.4),(.4,,5,-1.1,.4),...]
    sample=data[-1]
    # # print data
    if len(data)==1:
        peak_x,peak_y,peak_z,dip_x,dip_y,dip_z,range_x,range_y,range_z=sample[1],sample[2],sample[3],sample[1],sample[2],sample[3],0,0,0

    else:
    #     # print range_z
        
    #     # print sample
    #     # peaks
    #     if sample[1]>peak_x:  
    #         peak_x=sample[1]
    #         range_x=peak_x - dip_x
        if sample[2]>peak_y:  
            peak_y=sample[2]
            range_y=peak_y - dip_y
    #     if sample[3]>peak_z:  
    #         peak_z=sample[3]
    #         range_z=peak_z - dip_z
    #     # dips
    #     if sample[1]<dip_x:  
    #         dip_x=sample[1]
    #         range_x=peak_x - dip_x
        if sample[2]<dip_y:  
            dip_y=sample[2]
            range_y=peak_y - dip_y
    #     if sample[3]<dip_z:
    #         dip_z=sample[3]
    #         range_z=peak_z - dip_z

        # print "%d, %d (peak,dip)" %(peak_z,dip_z)
        # last-half of cycle
        # defined by latest datum not being max or min and
        # if the up or down motion caused at least .4 g
        # print
        # if (range_x>.4) and (dip_x< sample[1] < peak_x):
        #     print "%f, %f, %f" % (range_x,range_y,range_z)
        #     axis =1
        #     halfway(axis,peak_x,dip_x)
        #     peak_x,peak_y,peak_z,dip_x,dip_y,dip_z,range_x,range_y,range_z=sample[1],sample[2],sample[3],sample[1],sample[2],sample[3],0,0,0
        # if (range_z>.8) and (dip_z< data[-1][3] < peak_z):
        #     print "%f, %f, %f" % (range_x,range_y,range_z)
        #     axis = 3
        #     halfway(axis, peak_z, dip_z)
        #     peak_x,peak_y,peak_z,dip_x,dip_y,dip_z,range_x,range_y,range_z=sample[1],sample[2],sample[3],sample[1],sample[2],sample[3],0,0,0  
        
        
    if len(data)>3:
        y_slope=get_slope(2)
        # print str(y_slope)
        d_slope=prev_y_slope- y_slope
        # if abs(y_slope)<.25 and abs(prev_y_slope)>.25:
        # print str(abs(d_slope))
        if  range_y>.4:
            if (prev_y_slope>0 and y_slope<0) or (prev_y_slope<0 and y_slope>0):
                print "peak with range: %f" % range_y
                peaks+=1
                print peaks
                if peaks==2:
                    if range_y>.80: 
                        exercise="curl"
                    else: 
                        exercise="latRaise"
                    rep_event(exercise)
                    peaks=0
                    del data[:-2]
                # halfway(axis, peak_y,dip_y)
                    peak_y, dip_y,range_z=sample[2],sample[2], 0
        prev_y_slope=y_slope
        # if (range_y>.3) and (dip_y< data[-1][3] < peak_y):
        #     # print "%f, %f, %f" % (range_x,range_y,range_z)
        #     axis = 2
        #     halfway(axis, peak_y,dip_y)
        #     # print "out of halfway"
        #     peak_x,peak_y,peak_z,dip_x,dip_y,dip_z,range_x,range_y,range_z=sample[1],sample[2],sample[3],sample[1],sample[2],sample[3],0,0,0      




            


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

        

if __name__ == '__main__':
    main()