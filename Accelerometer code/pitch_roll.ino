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

int servoPin = 7;      // Control pin for servo motor
int potPin   = 0;      // select the input pin for the potentiometer

int pulseWidth = 0;    // Amount to pulse the servo
long lastPulse = 0;    // the time in millisecs of the last pulse
int refreshTime = 20;  // the time in millisecs needed in between pulses
int val;               // variable used to store data from potentiometer

int minPulse = 500;   // minimum pulse width

const float alpha = 0.5;

double fXg = 0;
double fYg = 0;
double fZg = 0;

ADXL345 acc;

void setup()
{
	acc.begin();
        pinMode(servoPin, OUTPUT);  // Set servo pin as an output pin
        pulseWidth = minPulse;      // Set the motor position to the minimum
	Serial.begin(9600);
	delay(100);
}


void loop()
{
	double pitch, roll, Xg, Yg, Zg;
	acc.read(&Xg, &Yg, &Zg);

	//Low Pass Filter
	fXg = Xg * alpha + (fXg * (1.0 - alpha));
	fYg = Yg * alpha + (fYg * (1.0 - alpha));
	fZg = Zg * alpha + (fZg * (1.0 - alpha));

	//Roll & Pitch Equations
	roll  = (atan2(-fYg, fZg)*180.0)/M_PI;
	pitch = (atan2(fXg, sqrt(fYg*fYg + fZg*fZg))*180.0)/M_PI;

	Serial.print(pitch);
	Serial.print(":");
	Serial.println(roll);
        
//          val = analogRead(potPin);    // read the value from the sensor, between 0 - 1024
        val = roll;
        if (val > 0 && val <= 999 ) {
          pulseWidth = val*2 + minPulse;  // convert angle to microseconds
          
          Serial.print("moving servo to ");
          Serial.println(pulseWidth,DEC);
        }
        updateServo();   // update servo position
        
	delay(10);
}
// called every loop(). 
void updateServo() {
  // pulse the servo again if the refresh time (20 ms) has passed:
  if (millis() - lastPulse >= refreshTime) {
    digitalWrite(servoPin, HIGH);   // Turn the motor on
    delayMicroseconds(pulseWidth);  // Length of the pulse sets the motor position
    digitalWrite(servoPin, LOW);    // Turn the motor off
    lastPulse = millis();           // save the time of the last pulse
  }
}

