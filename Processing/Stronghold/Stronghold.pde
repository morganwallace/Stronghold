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

// Repetition counters for dumbbell input
int reps_1s = 0;
int previous_reps_1s = 0;

int reps_2s = 0;
int previous_reps_2s = 0;

int reps_1r = 0;
int previous_reps_1r = 0;

int reps_2r = 0;
int previous_reps_2r = 0;


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

// Game mode variable switches between "start", "run", "pause" and "end" screen
char mode = 'r';

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

// Draw screens (game itself as well as start and end screen)
void draw() {
  switch(mode) {
    case 's': //start
      startGame();
      break;
    case 'r':  //run
      runGame();
      break;
    case 'p': //pause
      pauseGame();
      break;
    case 'e': //end
      endGame();
      break;
  }
  /*
  if(gameOn) {
    runGame();
  }
  else{
    endGame();
  }
  */
}

// Draws the health bar
void drawHealthBar (int posx, int posy, float health) {
  fill(0,230,0,200);
  noStroke();
  rect(posx, posy, posx+health, posy+10);
}
