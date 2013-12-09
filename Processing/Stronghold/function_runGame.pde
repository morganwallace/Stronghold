// #### Main game logic, looped as long as game runs

void runGame() { 
  // Display background
  image(stronghold_bg, 0, 0);
  
  // Display castle
  castleOffset = castlehealth*castleOffsetMultiplier;
  image(castle_bg, 0, 100 - castleOffset);
  
  drawHealthBar(10, 10, castlehealth);

  knight1.display(); 
  knight2.display();
  sync1.display();
  sync2.display();   
  
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
  
  for (int i = explosions.size()-1; i >= 0; i--) {
    Explosion explosion = explosions.get(i);
    explosion.display();
    
    if(explosion.finished()) {
      explosions.remove(i);
    } 
  }
      
      
  // ##### DUMBBELL INPUT #####
  
  //Load rep data from file
  lines = loadStrings("player1shoot.txt");
  reps_1s=Integer.parseInt(lines[0]);
  if (reps_1s>previous_reps_1s){
      //Shoot only if the input conforms to the frequency of the sync object
      //i.e. if the key is hit when object is in the peak range 
      if (sync1.peak()){
        knight1.shoot(1);
        //change color of the object in order to identify positive identification
        sync1.load_image("red");
      }
    previous_reps_1s=reps_1s;
    //println(reps_1s);
  }
  
  lines = loadStrings("player2shoot.txt");
  reps_2s=Integer.parseInt(lines[0]);
  if (reps_2s>previous_reps_2s){
      //Shoot only if the input conforms to the frequency of the sync object
      //i.e. if the key is hit when object is in the peak range 
      if (sync2.peak()){
        knight2.shoot(2);
        //change color of the object in order to identify positive identification
        sync2.load_image("red");
      }
    previous_reps_2s=reps_2s;
    //println(reps_2s);
  }
  
  lines = loadStrings("player1repair.txt");
  reps_1r=Integer.parseInt(lines[0]);
  if (reps_1r>previous_reps_1r){
      //Repair only if the input conforms to the frequency of the sync object
      //i.e. if the key is hit when object is in the peak range 
      if (sync1.peak()){
      knight1.repair();
        //change color of the object in order to identify positive identification
        sync1.load_image("red");
      }
    previous_reps_1r=reps_1r;
    //println(reps_1r);
  }
  
  lines = loadStrings("player2repair.txt");
  reps_2r=Integer.parseInt(lines[0]);
  if (reps_2r>previous_reps_2r){
      //Repair only if the input conforms to the frequency of the sync object
      //i.e. if the key is hit when object is in the peak range 
      if (sync2.peak()){
      knight2.repair();
        //change color of the object in order to identify positive identification
        sync2.load_image("red");
      }
    previous_reps_2r=reps_2r;
    //println(reps_2r);
  }
  
  
  
  // ##### KEYBOARD INPUT #####
  
  if(keyPressed) {
    // Shoot arrow from player 1 if key 'A' is pressed
    if (key == 'a' || key == 'A') {
      //Shoot only if the input conforms to the frequency of the sync object
      //i.e. if the key is hit when object is in the peak range 
      if (sync1.peak()){
        knight1.shoot(1);
        //change color of the object in order to identify positive identification
        sync1.load_image("red");
      }
    }
    
    // Shoot arrow from player 2 if key 'B' is pressed
    if (key == 'l' || key == 'L') {
      //Shoot only if the input conforms to the frequency of the sync object
      //i.e. if the key is hit when object is in the peak range 
      if (sync2.peak()){
        knight2.shoot(2);
        //change color of the object in order to identify positive identification
        sync2.load_image("red");
      }
    }
    
    // Castle repair from player 1 if key 'Q' is pressed
    if (key == 'q' || key == 'Q') {
      //Repair only if the input conforms to the frequency of the sync object
      //i.e. if the key is hit when object is in the peak range 
      if (sync1.peak()){
      knight1.repair();
        //change color of the object in order to identify positive identification
        sync1.load_image("red");
      }
    }
    
    // Castle repair from player 2 if key 'O' is pressed
    if (key == 'o' || key == 'O') {
      //Repair only if the input conforms to the frequency of the sync object
      //i.e. if the key is hit when object is in the peak range 
      if (sync2.peak()){
      knight2.repair();
        //change color of the object in order to identify positive identification
        sync2.load_image("red");
      }
    }
    
    // Pause game if Space bar key is pressed
    if (key == ' ') {
      Date d = new Date();
      long currentTime = d.getTime();
      if(currentTime > lastPause + waitPause) {
        lastPause = currentTime;
        mode = 'p';
      }
     }
  }
}
