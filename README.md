#Arduino Dumbbell Accelerometer

##Overview
**This code will run on an Arduino Micro (Leonardo) with a  connected ADXL45 accelerometer**

The accelerometer will be attached to the dumbbell and sense motion in many directions and compute it into distinct motions and then abstract those into reps. Each rep must also be categorized by type of lifting movement. 

The goal is to make a **multiplayer tower-defense game** that is compelling enough to encourage more exersice.

##Members

Name | Email | Responsibility
------------ | ------------- | ------------
Morgan Wallace | morgan@ischool.berkeley.edu | Accelerometer and output visualization
Divya Karthikeyan | divyaanand@berkeley.edu | Accelerometer output
SUHAIB SAQIB SYED| susyed@berkeley.edu | Research and Wireframing
Clemens Meyer| clemens.meyer@ischool.berkeley.edu | Presentation and Game Design

---
##Specifics
###Games
**Stronghold** is an exercise game. 1 to 2 players lift weights attached with sensors that control the game. The game ends when skeletons destroy your 'Stronghold' by reaching your wall and exploding. Curls repair the castle and lateral raises shoot arrows at skeletons. 

**xyz_out_micro.ino** is another mod of the example code that instead outputs the forces (g) in each direction (x, y, and z) to the serial port every 50 ms.

### Python Viz
**accelerometer_make_sample.py** is a real-time visualization of x, y, and z acceleration in Gs. Uses [Matplotlib](http://matplotlib.org) to take parsed serial output and graph it
