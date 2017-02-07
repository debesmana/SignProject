Box[] BoxesArray = new Box[50];

IntDict concordance;

void setup() {
  size(500, 500);
  int FailCount = 0;
  
  //println(AllText.length);
  //  for(int i=0; i<AllText.length; i++){
  //    println(AllText[i]);
   // }
  for (int i = 0; i < BoxesArray.length; i++) {
    do {
      BoxesArray[i] = new Box(random(width-8), random(width-8));
      FailCount++;
      if (FailCount % 100 == 0) {
        println("WARN: Failed to place box " + FailCount + " times.");
        if (FailCount == 2500) {
          println("ERR: Run " + i + " failed to place box 2500 times. Exiting.");
          System.exit(1);
        }
      }
    } while (CheckBoxesOverlap(BoxesArray[i], i));
  }
}

void draw() {
  background(255);
  noLoop();
  for (int i=0; i<BoxesArray.length; i++) {
    BoxesArray[i].display();
  }
}

boolean BoxesOverlap(Box newBox, Box oldBox) {
  if (newBox.posX > oldBox.posX && newBox.posX + newBox.Size < oldBox.posX + oldBox.Size) { //if x overlaps
    if (newBox.posY > oldBox.posY && newBox.posY + newBox.Size < oldBox.posY + oldBox.Size) { //if y overlaps
      //println("Not on top of each other"); 
      return true;
    } else {
      return false;
    }
  } else {
    return false;
  }
}

boolean CheckBoxesOverlap(Box newBox, int Current) {
  if(Current == 0){
    return false;
  }
  
  for (int i = 0; i < Current; i++) {
    if (BoxesArray[i] != null) {
      if (BoxesOverlap(newBox, BoxesArray[i])) {
        println("Here");
        return true;
      }
    } else {
      println("Null, breaking execution.");
      break;
    }
  }
  return false;
}