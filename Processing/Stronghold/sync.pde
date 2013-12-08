//Author: Suhaib Saqib Syed
//Date: 12/6/2013
//Purpose: Create a sync indicator to promote a rhythm 
//Inputs: Indicator start position
//        Indicator frequency (integer which is converted into radians)
//Outputs: An object moving at a set frequency
//

class Sync{
PImage image;    //Image object 
String colour;   //To choose a different png based on color

//Position related variables
float ypos;      //Initial Y-Position 
float xpos;      //Initial X-Position 
float y;         //Current position 
float freq;      //Frequency of the cycle
float angle = 0; //Cosine angle initialization 

boolean peak;    //Detecting if the object is at the peak of the cycle
boolean top_reached; 
boolean bottom_reached;

Sync( float xpos_my, float ypos_my, float freq_my){
 ypos = ypos_my;
 xpos = xpos_my;
 freq = freq_my;
 load_image("blue");    
}

void display(){
    float ang = radians(angle);
//Calculate the current positon of the object
    y = ypos + (50 * cos(ang));
//Load the image at the positio calculated 
    image(image, xpos , y);   
//Check if the object is in the peak range currently range set to +-40 
    if (y <= ypos - 40){
      peak = true;     
    } else {
      peak = false;
    }
//Reset the image  
    load_image("blue");
//Increment the angle by freq
    angle += freq;
}

boolean peak(){
//function to query whether the object is in the peak range  
return peak;
}

void load_image(String colour){
//Load the images based on the color specified and the direction of the object  
 String direction; 
 String path;
 
 //Query current Y-position to set top or bottom reached and change direction
  if (y == ypos + 50){
     top_reached = true;
     bottom_reached = false;
   } else if (y == ypos - 50){
     top_reached = false;
     bottom_reached = true;
   }
   
 //change directions
 if (top_reached){
 direction = "up";
 } else {
 direction = "down";}
 
 //set image path
 path = "../../Assets/progress_"+colour+"_"+direction+".png";
 // load image using path
 image = loadImage(path);
 // scale images by screen_scale factor
 image.resize(round(image.width*screen_scale),round(image.height*screen_scale));
}
}
