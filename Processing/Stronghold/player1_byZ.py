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

player=1
serPort='/dev/tty.usbmodem14'+str(player)+'1'
if player==1:
    dominant_axis=2
elif player==2:
    dominant_axis=2
#Attempt serial connection
try:
    ser = serial.Serial(serPort, 9600)

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
    del data[:-1]

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


peaks=0
prev_slope=0
peak,dip,peak_range=0,0,0
def detect_rep():
    """Use changes in slope to find peaks. 
    After a second peak is detected, trigger the rep_event function

    """
    global data,peak,dip,peak_range
    global prev_slope
    global peaks
    
    #data  looks like [(.2,,5,-1.1,.4),(.4,,5,-1.1,.4),...]
    sample=data[-1]
    # initialize the data for the first sample
    if len(data)==1:
        peak,dip,peak_range=sample[dominant_axis],sample[dominant_axis],0

    else:
        if sample[dominant_axis]>peak:  
            peak=sample[dominant_axis]
            peak_range=peak - dip
        # dips
        if sample[dominant_axis]<dip:  
            dip=sample[dominant_axis]
            peak_range=peak - dip

    if len(data)>3:
        y_slope=get_slope(dominant_axis)
        # print str(y_slope)
        d_slope=prev_slope- y_slope
        if  peak_range>.4:
            if (prev_slope>0 and y_slope<0) or (prev_slope<0 and y_slope>0):
                print "peak with range: %f" % peak_range
                peaks+=1
                # print peaks
                if peaks==2:
                    if peak_range>.90: 
                        exercise="curl"
                    else: 
                        exercise="latRaise"
                    rep_event(exercise)
                    peaks=0
                    peak, dip,range_z=sample[dominant_axis],sample[dominant_axis], 0
        prev_slope=y_slope
        

def main():
    global data
    global sampleRate
    global max_rep_window

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