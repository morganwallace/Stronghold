class Knight {
  PImage image;
  float xpos;
  float ypos;
  float damage = 5;   // Damage from each shot
  int wait = 500;     // Time between shots
  int lastShot = 0;   // Stores the time of the last shot

  Knight(float xpos_my, float ypos_my) {
    image = loadImage("../../Assets/knight.png");
    xpos = xpos_my;
    ypos = ypos_my;  
  }
  
  void display() {
    image(image, xpos, ypos);
  }
  
  // Function to shoot an enemy with an arrow
  void shoot() {
    // Figure out if waited long enough
    if(millis() > lastShot + wait) {
      lastShot = millis();
      
      /*
      // Display black overlay to indicate shot
      fill(0, 0, 0);
      rect(0, 0, width, height);
      */
      
      // Figure out which enemy is closest
      int closestEnemy = skeletons[0].index;
      for(int i=1; i<skeletons.length; i++) {
        if(skeletons[i].xpos < skeletons[closestEnemy].xpos ) {
          closestEnemy = skeletons[i].index;
        }
      }
      
      // Play flying arrow animation
      shootArrow(skeletons[closestEnemy]);      
      
      // Damage closest enemy 
      skeletons[closestEnemy].getHit(damage);
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
