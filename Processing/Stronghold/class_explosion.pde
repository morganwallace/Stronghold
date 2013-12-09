class Explosion {
  PImage e0,e1,e2,e3,e4,e5,e6,e7,e8,e9;
  float xpos;
  float ypos;
  
  Skeleton target;
  
  int index;
  boolean finished = false;
  
  Explosion(Skeleton target_my, int index_my) {
    // load images for arrow
    e6 = loadImage("../../Assets/Explosion/explosion6.png");
    
    // scale images by character_scale factor
    e6.resize(round(e6.width*character_scale),round(e6.height*character_scale));
    
    target = target_my;
    
    float xpos = target.xpos + target.image_m.width/2;
    float ypos = target.ypos + target.image_m.height/2;
            
    index = index_my;
    
  }
    
  void display() {
    image(e6, xpos, ypos);
  }
  
  
  boolean finished() {
    return finished;
  }
  
}
