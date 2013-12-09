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
PImage castle_bg;
PImage healthbar;
PImage startscreen;
PImage pausescreen;
PImage endscreen;
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
ArrayList<Explosion> explosions;
int explosionnumber = 1;
Sync sync1, sync2;
high_score high_score;

// Screen setup
float screen_scale = 1.5;      // Scaling factor when drawing the screen
float character_scale = screen_scale * 2;   // Scaling factor when drawing the characters
int screenwidth = round(640*screen_scale);
int screenheight = round(480*screen_scale);

// Game setup
float castleborder = screenwidth*0.2;  // X coordinate of the wall of the castle
float castlehealthinit = 100;        // Initial health of the castle
float castlehealth;
float castlehealthMax = 200;         // Maximum health of the castle
float castleOffsetMultiplier = 0.5;  // To calculate the offset from the castle health
float castleOffset = castlehealthinit * castleOffsetMultiplier;  // Offset of castle due to health
float gamespeed = 1.5;
float walkingspeed = 0.2; 
int skeleton_number = 8;

// Game mode variable switches between "start", "run", "pause" and "end" screen
char mode;

// Positioning of monsters
int y_start_position;
int y_start_upper = round(80*screen_scale);
int y_start_lower = round(screenheight - 20*character_scale);

// Variables to avoid repeat triggering of key events
long lastPause = 0;
long waitPause = 500;

// Score keeping variables
int global_score = 0;
String global_team = "Team Stronghold";
String global_p1 = "Suhaib";
String global_p2 = "Morgan";
int call_count = 0; 

// Game setup, runs once on launch
void setup() {
  
  // Basic screen setup
  size(screenwidth, screenheight);
  background(0,0,0);
  frameRate(30);
  
  // Load and resize background image
  stronghold_bg = loadImage("../../Assets/stronghold_bg.png");
  stronghold_bg.resize(round(stronghold_bg.width*screen_scale),round(stronghold_bg.height*screen_scale));
  
  // Load and resize castle image
  castle_bg = loadImage("../../Assets/castle.png");
  castle_bg.resize(round(castle_bg.width*screen_scale),round(castle_bg.height*screen_scale));
  
  // Load and resize healthbar image
  healthbar = loadImage("../../Assets/healthbar.png");
  healthbar.resize(round(healthbar.width*screen_scale),round(healthbar.height*screen_scale));
  
  // Load and resize pause screen image
  startscreen = loadImage("../../Assets/startscreen.png");
  startscreen.resize(round(startscreen.width*screen_scale),round(startscreen.height*screen_scale));

  // Load and resize pause screen image
  pausescreen = loadImage("../../Assets/pausescreen.png");
  pausescreen.resize(round(pausescreen.width*screen_scale),round(pausescreen.height*screen_scale));

  // Load and resize end screen image
  endscreen = loadImage("../../Assets/endscreen.png");
  endscreen.resize(round(endscreen.width*screen_scale),round(endscreen.height*screen_scale));

  // Load and resize explosion image
  explosion = loadImage("../../Assets/explosion.png");
  explosion.resize(round(explosion.width*character_scale),round(explosion.height*character_scale));
  
  // Initialize two knights with variable coordinates
  knight1 = new Knight(width/6, height/8+castleOffset*3, 1);
  knight2 = new Knight(width/6, height/3+castleOffset*3, 2);
  
  // Initialize syncs with variable coordinates and frequency
  sync1 = new Sync(width/6, height/7, 2, knight1);
  sync2 = new Sync(width/6, height/2.7, 2, knight2); 
  
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
  
 // Create array list (= array of variable length) of explosions
  explosions = new ArrayList<Explosion>(); 
  
  reset();
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
}

// Draws the health bar
void drawHealthBar (int posx, int posy, float health) {
  if(castlehealth > castlehealthinit * 0.4) {
    fill(0,230,0,200);
  } else {
    fill(190,0,0,200);
  }
  noStroke();
  rect(posx, posy, posx+health, posy+10);
  image(healthbar, 0, 0); // Draw healthbar image
}
