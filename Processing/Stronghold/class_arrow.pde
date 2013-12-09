class Arrow {
  PImage image;
  float xpos;
  float ypos;
  
  Knight origin;
  Skeleton target;
  
  float startx;
  float starty;
  float endx;
  float endy;
    
  float speed = 10 * gamespeed;
  float angle;
  
  float pathlength;  // length of the path that the arrow travels
  
  int index;
  boolean finished = false;
  
  Arrow(Knight origin_my, Skeleton target_my, int index_my) {
    // load image for arrow
    image = loadImage("../../Assets/arrow.png");
    
    // scale images by character_scale factor
    image.resize(round(image.width*character_scale),round(image.height*character_scale));
    
    origin = origin_my;
    target = target_my;
    
    float startx = origin.xpos + origin.image1.width;
    float starty = origin.ypos + origin.image1.height/2 - castleOffset;
    float endx = target.xpos;
    float endy = target.ypos + target.image_m.height/2;
    
    xpos = startx;
    ypos = starty;
        
    index = index_my;
    
    pathlength = sqrt((endx-startx)*(endx-startx) + (endy-starty)*(endy-starty));
    //println("Arrow path length: " + pathlength);
    angle = atan((endy-starty)/(endx-startx));
    //println("Arrow angle: " + angle/(PI/2));
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
    if (xpos < target.xpos) {
      xpos += speed;
      ypos += speed*tan(angle);
    }
    else {
      target.getHit(origin.damage);
      finished = true;
      //keeping score
      global_score = global_score + 1;
    }
  }
  
  boolean finished() {
    return finished;
  }
  
}
