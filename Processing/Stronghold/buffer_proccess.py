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
start_time=time.time()
######  Preferences Variables  ######
sampleRate=.2 #this is set by the code on Arduino
max_rep_window=5 #seconds
min_rep_window=.4 #seconds
initialize_time=1 #second


ser = serial.Serial('/dev/tty.usbmodem1421', 9600)
# ser_toProcessing=serial.Serial('/dev/tty.usbmodem1422', 9600)
# time.sleep(.5)

def timer():
	global start_time
	return time.time()-start_time

def get_data_from_serial():
    serialOutput=ser.readline()
    # print serialOutput
    serialTuple=serialOutput.split(",")
    if len(serialTuple)!=3:
        return None
    for i in range(len(serialTuple)):
        try:serialTuple[i]=float(serialTuple[i].strip())
        except: return None
    # print s
    x, y, z = serialTuple[0],serialTuple[1],serialTuple[2]
    t=timer()
    # print t,x,y,z
    return t,x,y,z

def get_slope(axis, samples=2):
	rise=data[-1][axis] - data[-samples][axis] #acc value, for x, i=1;    y, i=2;    z, i=3
	run=data[-1][0] - data[-samples][0] #time change
	return rise/run

def rep_event(root_times=(0,0,0)):
	global reps
	global data
	reps+=1
	print "reps: "+str(reps)
	del(data[:-1])
	with open('to_processing.txt','w') as out_file:
		out_file.write(str(reps))

	# serial_out_data="%f,%f,%f\n"%(root_times)
	# print 'test1'
	# ser.write("reps:"+str(reps))
	# print 'test'
	# test=ser.readline()
	# print test 


def main():
	global data
	global reps
	global sampleRate
	global max_rep_window
	global min_rep_window
	global start_time

	#loops forever
	while True:
		#limit time for rep detection to 5 seconds
		if len(data)*sampleRate>=max_rep_window: 
			del data[0]


		# if time.time()<start_time+1:
		# 	time.sleep(sampleRate)
		# 	continue
		# elif:
		# 	print "begin!\n"

		#Get time, x, y, and z from serial port
		data.append(get_data_from_serial())

		#Peak detection
		# detection=peak_detection()
		# if detection ==True:
		# 	data

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

					#direction of slope can tell you what to expect
					if get_slope(axis) > 0:
						curve="valley"
					else:
						curve ="hill"
					# print curve
					
					#get the time for this point - halfway through the rep
					halftime=timer()

					#wait and look for return to starting point
					while timer()-halftime<=max_rep_window/2:
						data.append(get_data_from_serial())
						if curve == "valley":
							if data[-1][axis] >=peak-.2:
								
								# rep_event(get_times(root1,root2,root3))
								rep_event()
								break
						elif curve == "hill":
							if data[-1][axis] <=dip+.2:
								rep_event()
								break
			
			
		while timer()<=data[-1][0]+sampleRate:
			pass
		


main()
if __name__ == '__main__':
	main()