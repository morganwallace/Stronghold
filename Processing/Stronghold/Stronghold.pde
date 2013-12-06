/* Stronghold Game
 * 
 * Defend the castle from the enemies!
 * Use the 'A' button on your keyboard to shoot them.
 * The game is over when the castle is too damaged.
*/

PImage stronghold_bg;
PImage explosion;

Knight knight1, knight2;
Skeleton[] skeletons;
ArrayList<Arrow> arrows;
int arrownumber = 1;

float castleborder = 190;  // X coordinate of the wall of the castle
float castlehealth;        // Health of the castle
boolean gameOn;            // If false, game is over
float gamespeed = 1.0;
float walkingspeed = 0.2;
float monster_scale = 2.0; // Scaling factor when drawing the monsters 
int skeleton_number = 8;

void setup() {
  size(640, 480);
  background(0,0,0);
  frameRate(30);
  
  castlehealth = 100;
  gameOn = true;
  
  stronghold_bg = loadImage("../../Assets/stronghold_bg.png");
  explosion = loadImage("../../Assets/explosion.png");
  
  knight1 = new Knight(width/6, height/8); //changed the co-ordinated based on width and height proportions
  knight2 = new Knight(width/6, height/3); //added new knight
  
  // Create array of skeletons (with random speed)
  skeletons = new Skeleton[skeleton_number];
  for (int i = 0; i < skeletons.length; i++) {
    skeletons[i] = new Skeleton(width, (i+1)*50+20, random(0.5, 1.5), 10, i);
  }
  
  arrows = new ArrayList<Arrow>(); 
}

void draw() {
  if(gameOn) {
    image(stronghold_bg, 0, 0);
    
    drawHealthBar(10, 10, castlehealth);
  
    knight1.display(); 
    knight2.display();
       
    for (int i = 0; i < skeletons.length; i++) {
      skeletons[i].display();
      skeletons[i].move();
    }
    
    for (int i = arrows.size()-1; i >= 0; i--) {
      Arrow arrow = arrows.get(i);
      arrow.display();
      arrow.move();
      
      if(arrow.finished()) {
        arrows.remove(i);
      }
      
    }
    
    if(keyPressed) {
      if (key == 'a' || key == 'A') {
        knight1.shoot();
      }
      
      if (key == 'l' || key == 'L') {
        knight2.shoot();
      }
      
    }
  
  }
  else{
    gameOver();
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
