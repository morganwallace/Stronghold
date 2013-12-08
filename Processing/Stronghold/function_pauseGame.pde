long lastPause = 0;
long waitPause = 500;

// Called when game is started
void pauseGame() {
  
  // Draw background
  image(stronghold_bg, 0, 0);

  // Draw transparent black box over it
  fill(0, 0, 0, 200);
  noStroke();
  rect(0, 0, width, height);
  
  // Figure out if waited long enough

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
