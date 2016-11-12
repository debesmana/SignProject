Box[] BoxesArray= new Box[50];
int Current = 0;

void setup(){
  size(500,500);
  /*for (int i=0; i<BoxesArray.length; i++){
    //find a better way to make sure it isn't drawn off screen
    println(BoxesArray[25]);
    BoxesArray[i] = new Box(random(width-8),random(width-8));
  }*/
  
  int FailCount = 0;
    
  for(int i = 0; i < BoxesArray.length; i++){
    Current = i;
    do {
      BoxesArray[i] = new Box(random(width-8),random(width-8));
      FailCount++;
      if(FailCount % 100 == 0){
        println("WARN: Failed to place box " + FailCount + " times.");
        if(FailCount == 2500){
          println("ERR: Failed to place box 2500 times. Exiting.");
          System.exit(1);
        }
      }
    }
    while (CheckBoxesOverlap(BoxesArray[i]));
  }
  
}

void draw(){
  background(255);
  noLoop();
  for (int i=0; i<BoxesArray.length; i++){
    BoxesArray[i].display();
  }  
}

/*newBox = bounds you are trying to draw,
oldBox = bounds you are comparing to in your array*/
boolean BoxesOverlap(Box newBox , Box oldBox) {
  if(newBox.posX > oldBox.posX && newBox.posX + newBox.Size < oldBox.posX + oldBox.Size/*It's almost 2, I doubt my logic is anywhere near ok. just compare the X values for overlap.*/){
     if(newBox.posY > oldBox.posY && newBox.posY + newBox.Size < oldBox.posY + oldBox.Size/*check if Y positions overlap*/){
        return true;/*fail, choose new position.
        On fail, add 1 to a failure counter,
        which is cleared when the box is drawn.
        When fail counter reaches 100 or 200,
        etc print a warning to the log.
        Quit trying to draw the square after failing
        1000 consecutive times.*/
     } else {
        return false;//draw
     }
  } else {
      return false;//draw
  }
}

boolean CheckBoxesOverlap(Box newBox){
  for(int i = 0; i < Current; i++){
    if(BoxesArray[i] != null){
      if(BoxesOverlap(newBox, BoxesArray[i])){
        return true;
      }
    } else {
      return false;
    }
  }
    return false;
}