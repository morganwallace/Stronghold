// Called when game is over
void endGame() {
  // Draw background
  image(stronghold_bg, 0, 0);

  // Draw transparent black box over it
  fill(0, 0, 0, 200);
  noStroke();
  rect(0, 0, width, height);
<<<<<<< HEAD
  
  // Add pause screen image over it
  image(endscreen, 0, 0);
=======
>>>>>>> a6ce7441a97315854ed641f464f73c0843fb2cb4
}
