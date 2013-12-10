//Author: Suhaib Saqib Syed
//Date: 12/9/2013
//Purpose: To read and write input from keyboard 
//Inputs: key press
//Outputs: save data to global variables on press of return key
//Note: This function is automatically called by the processing compiler on keyboard event

void keyPressed() {
String saved;  
  if (input_done == false) {
  // If the return key is pressed, save the String and clear it
   saved = global_typing;
  if (key == '\n' ) {
    switch(global_label2) {
    case 'T':
      if (global_typing != ""){
        //set global variable team name
        global_team = saved;
        //change label
        global_label2 = '1';
        global_label = "Player 1:";
        break;
       }
    case '1':
      if (global_typing != ""){
        //set global variable player 1
        global_p1 = saved;  
        //change label
        global_label = "Player 2:";
        global_label2 = '2';
        break;
       }    
    case '2':
      if (global_typing != ""){
       //set global variable player 2
       global_p2 = saved;
       global_label = "Press enter to save";
       global_label2 = '3';
       break;    
      }     
    case '3':
       input_done = true;
       break;              
    }
    // A String can be cleared by setting it equal to ""
    global_typing = ""; 
  } else if (keyCode == BACKSPACE && global_typing.length() > 0){
    //Backspace functionality
    global_typing = global_typing.substring(0, global_typing.length() - 1);
  } else {
    // Otherwise, concatenate the String
    // Each character typed by the user is added to the end of the String variable.
    global_typing = global_typing + key; 
  }
}
}
