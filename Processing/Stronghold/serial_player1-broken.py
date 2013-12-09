from __future__ import division
import serial
import time
import os
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
reps=0
reps2=0
start_time=time.time()
######  Preferences Variables  ######
sampleRate=.2 #this is set by the code on Arduino
max_rep_window=5 #seconds
min_rep_window=.4 #seconds
initialize_time=1 #second

ser = serial.Serial('/dev/tty.usbmodem1421', 9600)



def timer():
	global start_time
	return time.time()

def get_data_from_serial(serial):
    serialOutput=serial.readline()
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


def get_slope(axis,datalist, samples=2):
	rise=datalist[-1][axis] - datalist[-samples][axis] #acc value, for x, i=1;    y, i=2;    z, i=3
	run=datalist[-1][0] - datalist[-samples][0] #time change
	return rise/run

def rep_event(exer, root_times=(0,0,0),player=1):
    global data
    del data[:-2]

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


def calc_reps():

    #only look for reps after the min rep window
    min_samples=int(min_rep_window/sampleRate)
    if len(data)>=min_samples:

        #find max and min for each axis - !must be a more effiecient way!
        range1,range2,range3=(1,0,0,0),(2,0,0,0),(3,0,0,0)
        values=[]
        for axis in (1,2,3):
            #isolate data for axis
            values.append([t[axis] for t in data])
            #get max
            peak=max(values[axis-1])
            #get min
            dip=min(values[axis-1])
            if axis ==1:
                range1=(1,peak,dip,peak-dip)
                # print str(axis)+" "+str(range1)  
            if axis ==2:
                range2=(2,peak,dip,peak-dip)
                # print str(axis)+" "+str(range2)
            if axis ==3:
                range3=(3, peak,dip,peak-dip)
                # print str(axis)+" "+str(range3)

            #axis num, peak, dip, range
            biggest_range=(0,0,0,0)
            for r in (range1,range2,range3):
                if r[3]>biggest_range[3]:
                    biggest_range=(r[0],r[1],r[2],r[3])

            #More efficient but complicated way
            # elif len(data)>min_samples:
            # 	if data[-1][1]>xmax:xmax=data[-1][1]
            # 	if data[-1][2]>xmax:xmax=data[-1][2]
            # 	if data[-1][3]>xmax:xmax=data[-1][3]

                # last-half of cycle
                # defined by latest datum not being max or min and
                # if the up or down motion caused at least .4 g
        # peak_found = max(range1[2],range2[2],range3[2])
        print biggest_range
        if (biggest_range[3]>.6) and (biggest_range[2]< values[biggest_range[0]-1][-1] < biggest_range[1]):
            # exercise=axis  
            print "haflway"
            biggest_range=(0,0,0,0)             
            if range3[3]<0.5:
                exercise = 3
            else:
                exercise = 2
            # print axis
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
                data.append(get_data_from_serial(ser))
                print data[-1][biggest_range[0]]
                print curve
                if curve == "valley":
                    if data[-1][biggest_range[0]] >=biggest_range[1]-.1:
                        rep_event(exercise)
                        break

                elif curve == "hill":
                    if data[-1][biggest_range[0]] <=biggest_range[2]+.1:
                        rep_event(exercise)
                        break
        


def main():
    global data
    global sampleRate
    global max_rep_window

    #loops forever
    while True:
    	#limit time for rep detection to 5 seconds
        #print "start"
        last_sample=0
    	if len(data)*sampleRate>=max_rep_window: 
    		del data[0]
    		# del data2[0]
    	if time.time()>=last_sample+sampleRate:
        	#Get time, x, y, and z from serial port
        	data.append(get_data_from_serial(ser))

        if data:
            calc_reps()
            # print data[-1]
      
    		

if __name__ == '__main__':
	main()
