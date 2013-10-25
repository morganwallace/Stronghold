/*
 * Arduino to DB - Simple Version
 *
 * This project aims at reading input from a sensor and writing it to a CSV file.
 *
 */


int sensor = 0;
int val;

void setup() {
  Serial.begin(9600);
}

void loop() {
  val = analogRead(sensor);
  Serial.println(val);
}
