class Knight {
  PImage image;
  float xpos;
  float ypos;
  float damage = 10;   // Damage from each shot
  
  // Time-related variables
  long current;
  long lastShot = 0;   // Stores the time of the last shot
  long wait = 500;     // Time between shots

  Knight(float xpos_my, float ypos_my) {
    // Load and resize knight image (scaling divided by 2, as original image is larger)
    image = loadImage("../../Assets/knight.png");
    image.resize(round(image.width*character_scale/2),round(image.height*character_scale/2));

    xpos = xpos_my;
    ypos = ypos_my;  
  }
  
  void display() {
    image(image, xpos, ypos);
  }
  
  // Function to shoot an enemy with an arrow
  void shoot() {
    
    // Figure out if waited long enough
    Date d = new Date();
    current = d.getTime();
    if(current > lastShot + wait) {
      lastShot = current;

      // Figure out which enemy is closest
      int closestEnemy = skeletons[0].index;
      for(int i=1; i<skeletons.length; i++) {
        if(skeletons[i].xpos < skeletons[closestEnemy].xpos ) {
          closestEnemy = skeletons[i].index;
        }
      }
      
      // Shoot arrow
      shootArrow(skeletons[closestEnemy]);      
    }
  }
  
  
  void shootArrow(Skeleton enemy) {
    
    /*
    // Draw line from knight to enemy
    strokeWeight(5);
    stroke(0, 0, 0);
    line(startx, starty, endx, endy);
    */
    
    arrows.add(new Arrow(this, enemy, arrownumber));
    arrownumber++;
    
  }

}
