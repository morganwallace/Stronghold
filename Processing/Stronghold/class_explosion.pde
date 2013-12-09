class Explosion {
  //PImage e0,e1,e2,e3,e4,e5,e6,e7,e8,e9;
  PImage ex[];

  float xpos;
  float ypos;
  
  Skeleton target;
  
  int index;
  boolean finished = false;
  int counter;      // Display new image on every new frame
  
  Explosion(Skeleton target_my, int index_my) {
    ex = new PImage[10];

    // load images for arrow
    for (int i = 0; i<ex.length; i++) {
      ex[i] = loadImage("../../Assets/Explosion/explosion"+i+".png");
      ex[i].resize(round(ex[i].width*character_scale/2),round(ex[i].height*character_scale/2));
    }
      
    //e6 = loadImage("../../Assets/Explosion/explosion6.png");
    
    // scale images by character_scale factor
    //e6.resize(round(e6.width*character_scale/2),round(e6.height*character_scale/2));
    
    target = target_my;
    
    xpos = target.xpos - target.image_m.width/2;
    ypos = target.ypos - target.image_m.height/2;

            
    index = index_my;
    
  }
    
  void display() {
    image(ex[counter], round(xpos), round(ypos));
    counter++;
    if(counter == ex.length) {
      finished = true;
    }
  }
  
  
  boolean finished() {
    return finished;
  }
  
}
