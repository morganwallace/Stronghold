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
start_time=time.time()
######  Preferences Variables  ######
sampleRate=.2 #this is set by the code on Arduino
max_rep_window=5 #seconds
min_rep_window=.4 #seconds
initialize_time=1 #second


ser = serial.Serial('/dev/tty.usbmodem1421', 9600)
ser2=serial.Serial('/dev/tty.usbmodem1411', 9600)
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

def rep_event(player,exer, root_times=(0,0,0)):
    global reps
    global data
    global reps2
    global reps3
    global reps4
    if ((player==1) and (exer==2)):
        reps+=1
        print "Player1 shooting:" + "reps: "+str(reps)
        del(data[:-1])
        with open("player1shoot.txt" ,'w') as out_file:
            out_file.write(str(reps))
    elif ((player==1) and (exer !=2)):
        reps2+=1
        print "Player1 repair:" + "reps: "+str(reps2)
        del(data2[:-1])
        with open("player2repair.txt" ,'w') as out_file:
            out_file.write(str(reps2))
    elif ((player==2) and (exer==2)):
        reps3+=1
        print "Player2 shooting:" + "reps: "+str(reps3)
        del(data[:-1])
        with open("player2shoot.txt" ,'w') as out_file:
            out_file.write(str(rep3))
    elif ((player==2) and (exer !=2)):
        reps4+=1
        print "Player2 repair:" + "reps: "+str(reps4)
        del(data2[:-1])
        with open("player2repair.txt" ,'w') as out_file:
            out_file.write(str(reps4))

	# serial_out_data="%f,%f,%f\n"%(root_times)
	# print 'test1'
	# ser.write("reps:"+str(reps))
	# print 'test'
	# test=ser.readline()
	# print test 


def calc_reps(d):
    if d == 1:
        #only look for reps after the min rep window
        min_samples=int(min_rep_window/sampleRate)
        if len(data)>=min_samples:

            #find max and min for each axis - !must be a more effiecient way!
            for axis in (1,2,3):
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
                                rep_event(d, exercise)
                                break
                        elif curve == "hill":
                            if data[-1][axis] <=dip+.2:
                                rep_event(d, exercise)
                                break
    elif d==2:
        #only look for reps after the min rep window
        min_samples=int(min_rep_window/sampleRate)
        if len(data2)>=min_samples:

            #find max and min for each axis - !must be a more effiecient way!
            for axis in (1,2,3):
                #isolate data for axis
                for t in data2:
                    if t:
                        values=[t[axis] for t in data2]
                        #get max
                        peak=max(values)
                        #get min
                        dip=min(values)

                        #More efficient but complicated way
                        # elif len(data)>min_samples:
                        #   if data[-1][1]>xmax:xmax=data[-1][1]
                        #   if data[-1][2]>xmax:xmax=data[-1][2]
                        #   if data[-1][3]>xmax:xmax=data[-1][3]

                        # last-half of cycle
                        # defined by latest datum not being max or min and
                        # if the up or down motion caused at least .4 g
                        if (peak-dip>.6) and (dip< values[-1] < peak):
                            print axis
                            exercise = axis

                            #direction of slope can tell you what to expect
                            if get_slope(axis, data2) > 0:
                                curve="valley"
                            else:
                                curve ="hill"
                            # print curve

                            #get the time for this point - halfway through the rep
                            halftime=time.time()

                            #wait and look for return to starting point
                            while time.time()-halftime<=max_rep_window/2:
                                data2.append(get_data_from_serial(ser2))
                                if curve == "valley":
                                    if data2[-1][axis] >=peak-.2:

                                        # rep_event(get_times(root1,root2,root3))
                                        rep_event(d, exercise)
                                        break
                                elif curve == "hill":
                                    if data2[-1][axis] <=dip+.2:
                                        rep_event(d, exercise)
                                        break



def main():
    global data
    global data2
    global reps
    global reps2
    global reps3
    global reps4
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
        if len(data2)*sampleRate>=max_rep_window:
    		del data2[0]
    	#Get time, x, y, and z from serial port
    	data.append(get_data_from_serial(ser))
        data2.append(get_data_from_serial(ser2))
        if data:
            calc_reps(1)
        if data2:
            calc_reps(2)
        #while time.time()<=data[-1][0]+sampleRate:
        #    pass
        #while time.time()<=data2[-1][0]+sampleRate:
        #    pass
		

if __name__ == '__main__':
	main()
