// Called when game is started
void startGame() {
  // Draw background
  image(stronghold_bg, 0, 0);
  
  // Display castle
  castleOffset = castlehealth*castleOffsetMultiplier;
  image(castle_bg, 0, 100 - castleOffset);

  // Draw transparent black box over it
  fill(0, 0, 0, 200);
  noStroke();
  rect(0, 0, width, height);
  
  // Add pause screen image over it
  image(startscreen, 0, 0);
  
  
  // Unpause game if waited long enough
  if(keyPressed) {
    Date d = new Date();
    long currentTime = d.getTime();
    if(currentTime > lastPause + waitPause) {
      lastPause = currentTime;
      if (key == ' ') {
        mode = 'r';
      }
    }
  }
}
