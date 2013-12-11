//Author: Suhaib Saqib Syed
//Date: 12/9/2013
//Purpose: To read and write input from keyboard 
//Inputs: key press
//Outputs: display data entered
//Note: Actual input recording being done in keyPressed function

void read_input(){
  PFont f;
  f = createFont("GaramondPremrPro-Disp",30,true);  
  float indent = width/2.5;
  float offset = height/2.5;
  
  if (input_done == false){
  // Set the font and fill for text
  textFont(f);
  fill(255, 255, 255);
  
  // Display
  text("Congratulations! \nYour High Score is: "+global_score, indent, offset);
  text("Team name", indent - 200, offset + 100);
  text(global_team, indent - 200, offset + 150);
  text("Player 1", indent, offset + 100);
  text(global_p1, indent, offset + 150);
  text("Player 2", indent + 175, offset + 100);
  text(global_p2, indent + 175, offset + 150);
  text(global_label+global_typing,indent, offset + 200);
  }
}
