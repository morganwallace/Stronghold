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
data2=[]
slopes=[]
reps=0
reps2=0
reps3=0
reps4=0
start_time=time.time()
######  Preferences Variables  ######
sampleRate=.2 #this is set by the code on Arduino
max_rep_window=5 #seconds
min_rep_window=.4 #seconds
initialize_time=1 #second

try:
	ser = serial.Serial('/dev/tty.usbmodem1421', 9600)
	ser2=serial.Serial('/dev/tty.usbmodem1411', 9600)
	print "2 player mode"
except:
	try:
		ser = serial.Serial('/dev/tty.usbmodem1421', 9600)
		print "single player mode"
	except:
		ser2=serial.Serial('/dev/tty.usbmodem1411', 9600)
		print "single player mode"


# time.sleep(.5)

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
    # print s
    x, y, z = serialTuple[0],serialTuple[1],serialTuple[2]
    t=time.time()
    #print t,x,y,z
    return t,x,y,z


def get_slope(axis,datalist, samples=2):
	rise=datalist[-1][axis] - datalist[-samples][axis] #acc value, for x, i=1;    y, i=2;    z, i=3
	run=datalist[-1][0] - datalist[-samples][0] #time change
	return rise/run

def rep_event(exer, root_times=(0,0,0),player=1):
    global data
    del data[:-2]

    #record reps by player and also by event
    if exer!=2:
        
        with open("player"+str(player)+"shoot.txt" ,'r+') as out_file:
            file_reps=int(out_file.read())+1
            print "Player"+str(player)+" shooting:" + "reps: "+str(file_reps)
            out_file.seek(0)
            out_file.write(str(file_reps))

    elif exer ==2:
        with open("player"+str(player)+"repair.txt" ,'r+') as out_file:
            file_reps=int(out_file.read())+1
            print "Player"+str(player)+" repair:" + "reps: "+str(file_reps)
            out_file.seek(0)
            out_file.write(str(file_reps))

	# serial_out_data="%f,%f,%f\n"%(root_times)
	# print 'test1'
	# ser.write("reps:"+str(reps))
	# print 'test'
	# test=ser.readline()
	# print test 


def calc_reps(d):

    #only look for reps after the min rep window
    min_samples=int(min_rep_window/sampleRate)
    if len(data)>=min_samples:

        #find max and min for each axis - !must be a more effiecient way!
        for axis in (3,2,1):
            #isolate data for axis
            values=[t[axis] for t in data]
            #get max
            peak=max(values)
            #get min
            dip=min(values)

        #More efficient but complicated way
        # elif len(data)>min_samples:
        # 	if data[-1][1]>xmax:xmax=data[-1][1]
        # 	if data[-1][2]>xmax:xmax=data[-1][2]
        # 	if data[-1][3]>xmax:xmax=data[-1][3]

            # last-half of cycle
            # defined by latest datum not being max or min and
            # if the up or down motion caused at least .4 g
            if (peak-dip>.6) and (dip< values[-1] < peak):
                print axis
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
                    data.append(get_data_from_serial(ser))
                    if curve == "valley":
                        if data[-1][axis] >=peak-.2:

                            # rep_event(get_times(root1,root2,root3))
                            rep_event(exercise)
                            break
                    elif curve == "hill":
                        if data[-1][axis] <=dip+.2:
                            rep_event(exercise)
                            break




def main():
    global data
    global sampleRate
    global max_rep_window
    global min_rep_window
    global start_time

    #loops forever
    while True:
    	#limit time for rep detection to 5 seconds
        #print "start"
    	if len(data)*sampleRate>=max_rep_window: 
    		del data[0]
    		
    	#Get time, x, y, and z from serial port
    	data.append(get_data_from_serial(ser))

        if data:
            calc_reps(1)
            # print data[-1]
        #while time.time()<=data[-1][0]+sampleRate:
        #    pass
        #while time.time()<=data2[-1][0]+sampleRate:
        #    pass
		

if __name__ == '__main__':
	main()
