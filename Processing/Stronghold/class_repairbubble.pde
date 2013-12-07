class RepairBubble {
  PImage image;
  float xpos;
  float ypos;
  
  Knight origin;
  
  float startx;
  float starty;
  float endx;
  float endy;
    
  float speed = 10 * gamespeed;
  
  int index;
  boolean finished = false;
  
  RepairBubble(Knight origin_my, int index_my) {
    // load image for repair bubble
    image = loadImage("../../Assets/repair.png");
    
    // scale image by character_scale factor
    image.resize(round(image.width*character_scale),round(image.height*character_scale));
    
    origin = origin_my;
    
    float startx = origin.xpos;
    float starty = origin.ypos + origin.image.height;
    float endx = startx;
    float endy = 10;
    
    xpos = startx;
    ypos = starty;
        
    index = index_my;
  }
    
  void display() {
    image(image, xpos, ypos);
  }
  
  void move() {
    if (ypos > endy) {
      ypos -= speed;
    }
    else {
      finished = true;
    }
  }
  
  boolean finished() {
    return finished;
  }
  
}
