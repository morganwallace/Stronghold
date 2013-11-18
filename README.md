#Arduino Dumbbell Accelerometer

##Overview
**This code will run on an Arduino Uno connected to an ADXL45 attitute sensor**

The accelerometer will be attached to the dumbbell and sense motion in many directions and compute it into distinct motions and then abstract those into reps. Each rep must also be categorized by type of lifting movement. 

##Members

Name | Email | Responsibility
------------ | ------------- | ------------
Morgan Wallace | morgan@ischool.berkeley.edu  | Accelerometer and output visualization
Divya Karthikeyan |   | Accelerometer output
SUHAIB SAQIB SYED|| Research and Wireframing
Clemens Meyer|| Presentation and Game Design

---
##Specifics
* ###Games
**Tower Defense Game** is a simple python based game found on the <http://pygame.org> website.
Find the link to the original game here: 
<http://www.pygame.org/download.shtml>
* ###Accelerometer code
	* **pitch_role.ino** is a slight modification of the example code that was modified to run out of a usb port. It outputs the pitch and roll of the accelerometer to the serial port every 10 miliseconds. 
	 * **xyz_out** is another mod of the example code that instead outputs the forces (g) in each direction (x, y, and z) to the serial port every 10 ms.
* ###Arduino_to_DB_Simple
**Arduino_to_DB_Simple.ino** is a first attempt to put the data output from the serial monitor into a data storage system. 
* ### Python Viz
	* Real-time visualization of y-axis acceleration in Gs. Uses [Matplotlib](http://matplotlib.org) to take parsed serial output and graph it
