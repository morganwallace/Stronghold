#Python Viz

Make sure to run **xyz_out.ino** before executing Python scripts in this directory.

##accelerometer_make_sample.py
This python script will plot x, y, and z data along the x axis (time in seconds). 
####You can specify these variables:

	#modifiable variables
	runningTime=50 #seconds
	exerciseType="lateral_raise"
	movingWindow=False
  

Output files go in a folder **labeled_data** and then in another folder **[date&time+exerciseType]**