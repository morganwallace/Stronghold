class Knight {
  PImage image1;
  PImage image2;
  float xpos;
  float ypos;
  float damage = 10;   // Damage from each shot
  float repaired = 5;
  int type;            // Defines the image of the knight
  
  // Time-related variables
  long current;
  long lastShot = 0;   // Stores the time of the last shot
  long lastRepair = 0;   // Stores the time of the last repair
  long waitShoot = 500;     // Time between shots
  long waitRepair = 500;     // Time between repairs

  Knight(float xpos_my, float ypos_my, int type_my) {
    // Load and resize knight image (scaling divided by 2, as original image is larger)
    image1 = loadImage("../../Assets/knight1.png");
    image1.resize(round(image1.width*character_scale/2),round(image1.height*character_scale/2));
    image2 = loadImage("../../Assets/knight2.png");
    image2.resize(round(image2.width*character_scale/2),round(image2.height*character_scale/2));

    xpos = xpos_my;
    ypos = ypos_my;
    type = type_my;  
  }
  
  void display() {
    if(type == 1) {
      image(image1, xpos, ypos-castleOffset);
    }
    if(type == 2) {
      image(image2, xpos, ypos-castleOffset);
    }
  }
  
  // Function to shoot an enemy with an arrow
  void shoot(int rank) {
    
    // Figure out if waited long enough
    Date d = new Date();
    current = d.getTime();
    if(current > lastShot + waitShoot) {
      lastShot = current;

      // Figure out which enemy is closest
      int closestEnemy = skeletons[0].index;
      for(int i=1; i<skeletons.length; i++) {
        if(skeletons[i].xpos < skeletons[closestEnemy].xpos ) {
          closestEnemy = skeletons[i].index;
        }
      }
      
      // Figure out which enemy is second closest
      int secondClosestEnemy = skeletons[0].index;
      for(int i=1; i<skeletons.length; i++) {
        if(skeletons[i].xpos != skeletons[closestEnemy].xpos) { 
          if(skeletons[i].xpos < skeletons[secondClosestEnemy].xpos ) {
            secondClosestEnemy = skeletons[i].index;
          }
        }
      }

      // Shoot arrow at closest or second closest enemy, depending on rank variable
      if(rank == 1) {
        shootArrow(skeletons[closestEnemy]);
      }
      if(rank == 2) {
        shootArrow(skeletons[secondClosestEnemy]);
      }
      
    }
  }
  
  void shootArrow(Skeleton enemy) {
    arrows.add(new Arrow(this, enemy, arrownumber));
    arrownumber++;
  }
  
  void repair() {
    // Figure out if waited long enough
    Date d = new Date();
    current = d.getTime();
    if(current > lastRepair + waitRepair) {
      lastRepair = current;
      repairAnimation();
      if(castlehealth < castlehealthMax) {
        castlehealth += repaired;
      }
    }
  }

  void repairAnimation() {
    repairbubbles.add(new RepairBubble(this, repairnumber));
    repairnumber++;
  }

}
