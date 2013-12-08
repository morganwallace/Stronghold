<<<<<<< HEAD
// Called when game is started

=======
long lastPause = 0;
long waitPause = 500;

// Called when game is started
>>>>>>> a6ce7441a97315854ed641f464f73c0843fb2cb4
void pauseGame() {
  
  // Draw background
  image(stronghold_bg, 0, 0);

  // Draw transparent black box over it
  fill(0, 0, 0, 200);
  noStroke();
  rect(0, 0, width, height);
  
<<<<<<< HEAD
  // Add pause screen image over it
  image(pausescreen, 0, 0);
  
=======
>>>>>>> a6ce7441a97315854ed641f464f73c0843fb2cb4
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
