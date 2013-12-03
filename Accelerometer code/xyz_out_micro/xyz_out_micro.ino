/********************************************************************************
* ADXL345 Library Examples- pitch_roll.ino                                      *
*                                                                               *
* Copyright (C) 2012 Anil Motilal Mahtani Mirchandani(anil.mmm@gmail.com)       *
*                                                                               *
* License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html> *
* This is free software: you are free to change and redistribute it.            *
* There is NO WARRANTY, to the extent permitted by law.                         *
*                                                                               *
*********************************************************************************/

#include <Wire.h>
#include <ADXL345.h>

const float alpha = 0.5;

double fXg = 0;
double fYg = 0;
double fZg = 0;

ADXL345 acc;

void setup() {
        Wire.begin();
  	acc.begin();
	Serial.begin(9600);
        
         // while the serial stream is not open, do nothing:
        while (!Serial);
        Serial.println("start");

	delay(500);
}


void loop(){
  //read from the accelerometer and print to Serial as x,y,z
  
  
	double pitch, roll, Xg, Yg, Zg;
	acc.read(&Xg, &Yg, &Zg);

	//Low Pass Filter
	fXg = Xg * alpha + (fXg * (1.0 - alpha));
	fYg = Yg * alpha + (fYg * (1.0 - alpha));
	fZg = Zg * alpha + (fZg * (1.0 - alpha));

        Serial.print(fXg);
        Serial.print(",");
        Serial.print(fYg);
        Serial.print(",");
        Serial.print(fZg);
        Serial.println();   
        
        
	delay(10);
}
