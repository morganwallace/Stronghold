from __future__ import division
import serial
import time
import os

ser = serial.Serial('/dev/tty.usbmodem1421', 9600)
# time.sleep(.5)
def get_data_from_serial():
    serialOutput=ser.readline()
    # print serialOutput
    s=serialOutput.split(",")
    if len(s)!=3:
        return None
    for i in range(len(s)):
        try:s[i]=float(s[i].strip())
        except: return None
    # print s
    x, y, z = s[0],s[1],s[2]
    return x,y,z

def main():
	#loops forever
	while True:
		data=get_data_from_serial()
		ser.flush()
		print data
		# ser.write("from python " +str(data))
		# ser.flush()
		time.sleep(.2)
		


main()
if __name__ == '__main__':
	main()