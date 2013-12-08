// Called when game is started
void startGame() {
  // Draw background
  image(stronghold_bg, 0, 0);

  // Draw transparent black box over it
  fill(0, 0, 0, 200);
  noStroke();
  rect(0, 0, width, height);
  
  // Add pause screen image over it
  image(startscreen, 0, 0);
  
  
  if(keyPressed) {
    Date d = new Date();
    lastPause = d.getTime();
      if (key == ' ') {
        mode = 'r';
      }
  }
}
