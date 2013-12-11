//Author: Suhaib Saqib Syed
//Date: 12/8/2013
//Purpose: Create a sorted high score csv file 
//Inputs: Score, Team name, Player 1 name, Player 2 name
//Outputs: Sorted csv file of high scores

class High_score{

//Initialize tables  
Table score_table;
Table new_score_table;

//Initialize counts
int row_count;
int rank = 1;

//score keeping
int score;
String team_name;
String player1;
String player2;

boolean new_score_added = false;

High_score(int score_my, String team_name_my, String player1_my, String player2_my ){
  score = score_my;
  team_name = team_name_my;
  player1 = player1_my;
  player2 = player2_my;
}

void save_score() {
  call_count = call_count + 1;
  try {
  score_table = loadTable("high scores.csv", "header");
  //found high score table

  //create a new high score table with the same structure
  new_score_table = new Table();
  new_score_table.addColumn("Rank");
  new_score_table.addColumn("Team name");
  new_score_table.addColumn("Player1");
  new_score_table.addColumn("Player2");
  new_score_table.addColumn("Score");
  
  //loop through the current score table
  for (int i = 0; i < 9 && i < score_table.getRowCount(); i = i+1){
    //get each row of the current score table
    TableRow old_row = score_table.getRow(i);
  
    //check if the score of the current row is less than or equal to new score
    if (old_row.getInt("Score") <= score && new_score_added == false){
      //if yes, then insert the new entry at it's place in the new score table
      TableRow new_row = new_score_table.addRow();
      new_row.setInt("Rank", rank);
      new_row.setString("Team name", team_name);
      new_row.setString("Player1", player1);
      new_row.setString("Player2", player2);
      new_row.setInt("Score", score);
      // increment rank
      rank = rank + 1;
      new_score_added = true;
     }
  
    //transfer the old entry into the new table while preserving rest of the order
    TableRow new_row = new_score_table.addRow();
    new_row.setInt("Rank", rank);
    new_row.setString("Team name", old_row.getString("Team name"));
    new_row.setString("Player1", old_row.getString("Player1"));
    new_row.setString("Player2", old_row.getString("Player2"));
    new_row.setInt("Score", old_row.getInt("Score"));  
    // increment rank
    rank = rank + 1;
   }
  
  //Append the new score at the last position if it is the least score
  if (new_score_added == false){
    TableRow new_row = new_score_table.addRow();
    new_row.setInt("Rank", new_score_table.getRowCount());
    new_row.setString("Team name", team_name);
    new_row.setString("Player1", player1);
    new_row.setString("Player2", player2);
    new_row.setInt("Score", score);
   }
  
  //save table  
  saveTable(new_score_table, "data/high scores.csv");
  
  //display score
  display_score();  
  }
  catch (NullPointerException e){
    //If there is no high score table found  
    //create the table with the new entry
    score_table = new Table();
    //create the column headers
    score_table.addColumn("Rank");
    score_table.addColumn("Team name");
    score_table.addColumn("Player1");
    score_table.addColumn("Player2");
    score_table.addColumn("Score");
  
    //create the first entry
    TableRow new_row = score_table.addRow();
    new_row.setInt("Rank", rank);
    new_row.setString("Team name", team_name);
    new_row.setString("Player1", player1);
    new_row.setString("Player2", player2);
    new_row.setInt("Score", score);
  
    //save table
    saveTable(score_table, "data/high scores.csv");
    
    //display score
    display_score();
  }

}

void display_score(){
 Table display_table;
 float horizontal_offset = width/6;
 //Vertical offset
 float vertical_offset = height/2.5;
 //Font
 PFont f = createFont("GaramondPremrPro-Disp", 30, true); 
 
 display_table = loadTable("high scores.csv", "header");
  
  // Drawing properties
  textFont(f);       
  fill(255, 255, 255);
  textAlign(LEFT);
  
  for (TableRow display_row : display_table.rows()){
   text(display_row.getInt("Rank"), horizontal_offset, vertical_offset);
   text(display_row.getString("Team name"), horizontal_offset + 50, vertical_offset);
   text(display_row.getString("Player1"), horizontal_offset + 300, vertical_offset);
   text(display_row.getString("Player2"), horizontal_offset+ 450, vertical_offset);
   text(display_row.getInt("Score"), horizontal_offset + 600, vertical_offset);
   
   vertical_offset = vertical_offset + 40;

  }
}
}
