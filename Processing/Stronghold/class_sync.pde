//Author: Suhaib Saqib Syed
//Date: 12/6/2013
//Purpose: Create a sync indicator to promote a rhythm 
//Inputs: Indicator start position
//        Indicator frequency (integer which is converted into radians)
//Outputs: An object moving at a set frequency
//

class Sync{
PImage image;    //Image object 
PImage bg;  //Background of sync indicator
String colour;   //To choose a different png based on color

//Position related variables
float ypos;      //Initial Y-Position 
float xpos;      //Initial X-Position 
float y;         //Current position 
float freq;      //Frequency of the cycle
float angle = 0; //Cosine angle initialization 
float displayOffset;    //Offsets the image file to align the 'core' of the indicators when switching from up to down
float imageHeight;      //Needed to calculate the displayOffset

boolean peak;    //Detecting if the object is at the peak of the cycle
boolean top_reached; 
boolean bottom_reached;

Knight knight;  // To adjust position to knight

Sync( float xpos_my, float ypos_my, float freq_my, Knight knight_my){
  knight = knight_my;
  xpos = knight.xpos - width*0.01;
  ypos = knight.ypos + height*0.04;
  freq = freq_my;
  load_image("blue");    
  
  // load image for indicator background
  bg = loadImage("../../Assets/syncbar.png");
  
  // scale images by character_scale factor
  bg.resize(round(bg.width*character_scale/4),round(bg.height*character_scale/4));
  
}

void display(){
    
    // Display background bar
    stroke(0, 0, 0);
    strokeWeight(3);
    line(xpos, ypos-23-image.height-castleOffset, xpos+image.width, ypos-23-image.height-castleOffset); // upper end point
    line(xpos, ypos+32+image.height-castleOffset, xpos+image.width, ypos+32+image.height-castleOffset); // lower end point
    image(bg, xpos-7, ypos-castleOffset-64);
      

    float ang = radians(angle);
//Calculate the current positon of the object
    y = ypos - castleOffset + (50 * cos(ang));
//Load the image at the positio calculated 
    image(image, xpos, y+displayOffset);   
//Check if the object is in the peak range currently range set to +-40 
    if (y <= ypos - 40 - castleOffset){
      peak = true;     
    } else {
      peak = true;
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
  if (y == ypos - castleOffset + 50){
     top_reached = true;
     bottom_reached = false;
   } else if (y == ypos - castleOffset - 50){
     top_reached = false;
     bottom_reached = true;
   }
   
 //change directions
 if (top_reached){
   direction = "up";
   displayOffset = 0;
 } else {
   direction = "down";
   displayOffset = -19;
 }
 
 //set image path
 path = "../../Assets/progress_"+colour+"_"+direction+".png";
 // load image using path
 image = loadImage(path);
 // scale images by screen_scale factor
 image.resize(round(image.width*screen_scale),round(image.height*screen_scale));

 
}

}
