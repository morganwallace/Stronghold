// Called when game is over
void endGame() {
  
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
  image(endscreen, 0, 0);
  
  //Add some delay
  
  //Add data gathering (i.e. team name, player name)
  read_input();
  
  //Record and display scores
  if (call_count == 0 && input_done == true){
    high_score = new High_score(global_score, global_team, global_p1, global_p2);
    high_score.save_score();
  } else if (call_count >= 1){
    high_score.display_score();
  }
  
  // Delete all explosions
  for (int i = explosions.size()-1; i >= 0; i--) {
    Explosion explosion = explosions.get(i);
    explosions.remove(i);
  } 
  
  // Unpause game if waited long enough
  if(keyPressed) {
    Date d = new Date();
    long currentTime = d.getTime();
    if(currentTime > lastPause + waitPause) {
      lastPause = currentTime;
      if (key == ' ') {
        reset();
      }
    }
  }
}
