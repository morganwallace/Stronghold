class Arrow {
  PImage image;
  float xpos;
  float ypos;
  
  float startx;
  float starty;
  float endx;
  float endy;
    
  float speed = 10;
  
  float angle;
  
  float pathlength;  // length of the path that the arrow travels
  
  int index;
  
  Arrow(float startx_my, float starty_my, float endx_my, float endy_my, int index_my) {
    // load image for arrow
    image = loadImage("../../Assets/arrow.png");
    
    // scale images by monster_scale factor
    image.resize(round(image.width*monster_scale),round(image.height*monster_scale));
    
    startx = startx_my;
    starty = starty_my;
    endx = endx_my;
    endy = endy_my;
    
    xpos = startx;
    ypos = starty;
        
    index = index_my;
    
    pathlength = sqrt((endx-startx)*(endx-startx) + (endy-starty)*(endy-starty));
    //println("Arrow path length: " + pathlength);
    angle = atan((endy-starty)/(endx-startx));
    println("Arrow angle: " + angle/(PI/2));
  }
    
  void display() {
    
    // Rotate arrow (translation is necessary to rotate arrow around its own center) 
    /*
    translate(width/2, height/2);
    rotate(angle);
    translate(-width/2+xpos,-height/2+ypos);
    image(image, 0, 0);
    */
    image(image, xpos, ypos);
  }
  
  void move() {
    xpos += speed;
    ypos += speed*tan(angle);
  }
  
  boolean finished() {
    return false;
  }
  
}
