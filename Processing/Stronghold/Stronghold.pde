/* Stronghold Game
 * 
 * Defend the castle from the enemies!
 * Use the 'A' or 'L' button on your keyboard to shoot them.
 * Use the 'Q' or 'O' button to repair your castle.
 * The game is over when the castle is too damaged.
*/

// Import Java Date library
import java.util.Date;

PImage stronghold_bg;
PImage explosion;
String lines[];

int reps = 0;
int previous_reps = 0;

// Initialize objects
Knight knight1, knight2;
Skeleton[] skeletons;
ArrayList<Arrow> arrows;
int arrownumber = 1;
ArrayList<RepairBubble> repairbubbles;
int repairnumber = 1;

// Screen setup
float screen_scale = 1.5;      // Scaling factor when drawing the screen
float character_scale = screen_scale * 2;   // Scaling factor when drawing the characters
int screenwidth = round(640*screen_scale);
int screenheight = round(480*screen_scale);

// Game setup
float castleborder = screenwidth*0.3;  // X coordinate of the wall of the castle
float castlehealth = 100;        // Health of the castle
float castlehealthMax = 200;     // Maximum health of the castle
boolean gameOn;            // If false, game is over
float gamespeed = 1.5;
float walkingspeed = 0.2; 
int skeleton_number = 8;

// Positioning of monsters
int y_start_position;
int y_start_upper = round(80*screen_scale);
int y_start_lower = round(screenheight - 20*character_scale);

// Game setup, runs once on launch
void setup() {
  
  // Basic screen setup
  size(screenwidth, screenheight);
  background(0,0,0);
  frameRate(30);
  
  gameOn = true;
  
  // Load and resize background image
  stronghold_bg = loadImage("../../Assets/stronghold_bg.png");
  stronghold_bg.resize(round(stronghold_bg.width*screen_scale),round(stronghold_bg.height*screen_scale));

  // Load and resize explosion image
  explosion = loadImage("../../Assets/explosion.png");
  explosion.resize(round(explosion.width*character_scale),round(explosion.height*character_scale));
  
  // Initialize two knights with variable coordinates
  knight1 = new Knight(width/6, height/8);
  knight2 = new Knight(width/6, height/3);
  
  // Create array of skeletons
  skeletons = new Skeleton[skeleton_number];
  for (int i = 0; i < skeletons.length; i++) {
    // Set start position for skeletons
    y_start_position = y_start_upper + i * ( (y_start_lower - y_start_upper) / skeleton_number );   
    
    // Create skeletons. Parameters. x position, y position, speed (random), index
    skeletons[i] = new Skeleton(width, y_start_position, random(0.5, 1.5), i);
  }
  
  // Create array list (= array of variable length) of arrows
  arrows = new ArrayList<Arrow>();
 
 // Create array list (= array of variable length) of repair bubble
  repairbubbles = new ArrayList<RepairBubble>(); 
}

// Main game logic, looped as long as game runs
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
    
    for (int i = repairbubbles.size()-1; i >= 0; i--) {
      RepairBubble repairbubble = repairbubbles.get(i);
      repairbubble.display();
      repairbubble.move();
      
      if(repairbubble.finished()) {
        repairbubbles.remove(i);
      } 
    }
        
    //########## reps shoot skeletons
    
    //Load rep data from file
    lines = loadStrings("player1.txt");
    reps=Integer.parseInt(lines[0]);
    if (reps>previous_reps){
      knight1.shoot(1);
      previous_reps=reps;
      println(reps);
    }
    
    // Look for key presses
    if(keyPressed) {
      // Shoot arrow from player 1 if key 'A' is pressed
      if (key == 'a' || key == 'A') {
        knight1.shoot(1);
      }
      
      // Shoot arrow from player 2 if key 'B' is pressed
      if (key == 'l' || key == 'L') {
        knight2.shoot(2);
      }
      
      // Castle repair from player 1 if key 'Q' is pressed
      if (key == 'q' || key == 'Q') {
        knight1.repair();
      }
      
      // Castle repair from player 2 if key 'O' is pressed
      if (key == 'o' || key == 'O') {
        knight2.repair();
      }
      
    }
  
  }
  else{
    gameOver();
  }
}

// Draws the health bar
void drawHealthBar (int posx, int posy, float health) {
  fill(0,230,0,200);
  noStroke();
  rect(posx, posy, posx+health, posy+10);
}

// Called when game is over
void gameOver() {
  // Draw background
  image(stronghold_bg, 0, 0);

  // Draw transparent black box over it
  fill(0, 0, 0, 200);
  noStroke();
  rect(0, 0, width, height);
}
