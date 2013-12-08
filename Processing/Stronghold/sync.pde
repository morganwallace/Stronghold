//Author: Suhaib Saqib Syed
//Date: 12/6/2013
//Purpose: Create a sync indicator to promote a rhythm 
//Inputs: Indicator start position
//        Indicator frequency (integer which is converted into radians)
//Outputs: An object moving at a set frequency
//
class Sync{
PImage image;  
float ypos;
float xpos;
float freq;
boolean peak;
float angle = 0;
String image_path;

Sync( float xpos_my, float ypos_my, float freq_my){
 ypos = ypos_my;
 xpos = xpos_my;
 freq = freq_my;
 image_path = "../../Assets/progress_blue_up.png";
 load_image(image_path);    
}


void display(){
    float y;
    float ang = radians(angle);
    y = ypos + (50 * cos(ang));

    image(image, xpos , y);
   
    if (y <= ypos - 40){
      peak = true;  
      image_path = "../../Assets/progress_red_up.png";
      load_image(image_path);
    } else {
      peak = false;
      image_path = "../../Assets/progress_blue_up.png";
      load_image(image_path);
    }
   
    angle += freq;
}

boolean peak(){
return peak;
}

void load_image(String path){
 // load image using path
 image = loadImage(path);
 // scale images by screen_scale factor
 image.resize(round(image.width*screen_scale),round(image.height*screen_scale));
}
}
