/* Stronghold Game
 * 
 * Defend the castle from the enemies!
 * Use the 'A' button on your keyboard to shoot them.
 * The game is over when the castle is too damaged.
*/

import processing.serial.*;
Serial myPort;  // The serial port

PImage stronghold_bg;
PImage explosion;

Knight knight1;
Skeleton[] skeletons;

float castleborder = 190;  // X coordinate of the wall of the castle
float castlehealth;        // Health of the castle
boolean gameOn;            // If false, game is over
float gamespeed = 1.0;
float walkingspeed = 0.2;
float monster_scale = 2.0; // Scaling factor when drawing the monsters 

void setup() {
  myPort = new Serial(this, "/dev/tty.usbmodem1421", 9600);
  //Create Serial Object (9600 Baud)
  
  //Create a Wire Object
  //Wire.begin();


  size(640, 480);
  background(0,0,0);
  frameRate(30);
  
  castlehealth = 100;
  gameOn = true;
  
  stronghold_bg = loadImage("../../Assets/stronghold_bg.png");
  explosion = loadImage("../../Assets/explosion.png");
  
  knight1 = new Knight(100, 100);
  
  // Create array of skeletons (with random speed)
  skeletons = new Skeleton[4];
  for (int i = 0; i < skeletons.length; i++) {
    skeletons[i] = new Skeleton(width, (i+1)*100, random(0.5, 1.5), 10, i);
  }
}

void draw() {
  if(gameOn) {
    image(stronghold_bg, 0, 0);
    
    drawHealthBar(10, 10, castlehealth);
  
    knight1.display();  
       
    //Read in from Serial Port for accelerometer data
    while (myPort.available() > 0) {
      String inBuffer = myPort.readString();   
      if (inBuffer != null) {
        println(inBuffer);
        //split the serial output into an arrary of coordinates
        //String[] coords = inBuffer.split(",");
        //if (coords[1]>abs(.8);
      }
    }
       
    for (int i = 0; i < skeletons.length; i++) {
      skeletons[i].display();
      skeletons[i].move();
    }
    
    if(keyPressed) {
      if (key == 'a' || key == 'A') {
        knight1.shoot();
      }
    }
  
  }
  else{
    gameOver();
  }
}

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
  
  // Function to 
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
      int closestEnemy = skeletons[0].getIndex();
      for(int i=1; i<skeletons.length; i++) {
        if(skeletons[i].getXpos() < skeletons[closestEnemy].getXpos() ) {
          closestEnemy = skeletons[i].getIndex();
        }
      }
      // Damage closest enemy 
      skeletons[closestEnemy].getHit(damage);
    }
  }

}  
  
// Class that defines the "Skeleton" enemy
class Skeleton {
  PImage image_m;      // Image of monster in middle foot position
  PImage image_l;      // Image of monster in left foot position
  PImage image_r;      // Image of monster in right foot position
  float xpos;
  float ypos;
  float xspeed;
  float health;         // Current health of the monster
  float healthInit;     // Initial health of the monster
  float footpos = 0;      // Foot position
  int index;            // Index of the monster
  
  
  Skeleton(float xpos_my, float ypos_my, float xspeed_my, float health_my, int index_my) {
    // load images for walking character (left, middle and right foot position)
    image_m = loadImage("../../Assets/skeleton_m.png");
    image_l = loadImage("../../Assets/skeleton_l.png");
    image_r = loadImage("../../Assets/skeleton_r.png");
    
    // scale images by monster_scale factor
    image_m.resize(round(image_m.width*monster_scale),round(image_m.height*monster_scale));
    image_l.resize(round(image_l.width*monster_scale),round(image_l.height*monster_scale));
    image_r.resize(round(image_r.width*monster_scale),round(image_r.height*monster_scale));

    xpos = xpos_my;
    ypos = ypos_my;
    xspeed = xspeed_my;
    health = health_my;
    healthInit = health_my;
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
  
  float getXpos() { // Return X position of skeleton
    return xpos;
  }
  
  int getIndex() { // Return index of skeleton
    return index;
  }
  
  void explode() { // Triggers explosion
    image(explosion, xpos, ypos);
  }
  
  void getHit(float damage) {
    health -= damage;
    this.explode();
  }
}


void drawHealthBar (int posx, int posy, float health) { // Draws the health bar
  fill(0,230,0,200);
  noStroke();
  rect(posx, posy, posx+health, posy+10);
}

void gameOver() { // Called when game is over
  // Draw background
  image(stronghold_bg, 0, 0);

  // Draw transparent black box over it
  fill(0, 0, 0, 200);
  noStroke();
  rect(0, 0, width, height);
}
