//Author: Suhaib Saqib Syed
//Date: 12/6/2013
//Purpose: Create a sync indicator to promote a rhythm 
//Inputs: Indicator start position
//        Indicator frequency (integer which is converted into radians)
//Outputs: An object moving at a set frequency
//
class Sync{
  
float ypos;
float xpos;
float freq;
boolean peak;
float angle = 0;

Sync( float xpos_my, float ypos_my, float freq_my){
 ypos = ypos_my;
 xpos = xpos_my;
 freq = freq_my;
}


void display(){
    float y;
    float ang = radians(angle);
    y = ypos + (50 * cos(ang));
 
    fill(0, 250, 153);
    ellipse(xpos , y, 10, 10);
   
    if (y <= ypos - 40){
      peak = true;  
    } else {
      peak = false;
    }
   
    angle += 1;
}

boolean peak(){
return peak;
}
}
