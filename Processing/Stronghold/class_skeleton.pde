// Class that defines the "Skeleton" enemy
class Skeleton {
  PImage image_m;      // Image of monster in middle foot position
  PImage image_l;      // Image of monster in left foot position
  PImage image_r;      // Image of monster in right foot position
  float xpos;
  float ypos;
  float xspeed;
  float health = 10;         // Current health of the monster
  float healthInit;     // Initial health of the monster
  float footpos = 0;    // Foot position
  int index;            // Index of the monster
  
  
  Skeleton(float xpos_my, float ypos_my, float xspeed_my, int index_my) {
    // load images for walking character (left, middle and right foot position)
    image_m = loadImage("../../Assets/skeleton_m.png");
    image_l = loadImage("../../Assets/skeleton_l.png");
    image_r = loadImage("../../Assets/skeleton_r.png");
    
    // scale images by character_scale factor
    image_m.resize(round(image_m.width*character_scale),round(image_m.height*character_scale));
    image_l.resize(round(image_l.width*character_scale),round(image_l.height*character_scale));
    image_r.resize(round(image_r.width*character_scale),round(image_r.height*character_scale));

    xpos = xpos_my;
    ypos = ypos_my;
    xspeed = xspeed_my * gamespeed;
    healthInit = health;
    index = index_my;
  }
  
  void display() {
    // Display image depending on foot position
    if(footpos < 1) {
      image(image_m, xpos, ypos);
    } else
    if(footpos < 2) {
      image(image_l, xpos, ypos);
    } else
    if(footpos < 3) {
      image(image_m, xpos, ypos);
    } else
    if(footpos < 4) {
      image(image_r, xpos, ypos);
    }
  }
  
  void move() {
    // When dead, explode and reset
    if(health <= 0) {
      this.explode();
      this.reset();
    }
    
    // Move
    xpos = xpos - xspeed;
    
    // Switch foot position depending on game speed
    if (footpos < 3.8) {
      footpos += walkingspeed*gamespeed;
    }
    else {
      footpos = 0;
    }
    
    // If at castle, explode, cause damage and reset 
    if(xpos <= castleborder) {
     this.explode();
     this.reset();
     castlehealth -= 10;

     if(castlehealth <= 0) {
       gameOn = false;
     }
    } 
  }
  
  void reset() {
    xpos = width;
    health = healthInit;
  }
  
  void explode() { // Triggers explosion
    image(explosion, xpos-explosion.width/2, ypos-explosion.width/2);
  }
  
  void getHit(float damage) {
    health -= damage;
    this.explode();
  }
}
