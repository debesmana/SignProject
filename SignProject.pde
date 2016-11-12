Box[] mybox= new Box[50];

void setup(){
  size(500,500);
  for (int i=0; i<mybox.length; i++){
    //find a better way to make sure it isn't drawn off screen
    mybox[i] = new Box(random(width-8),random(width-8));
  }
}

void draw(){
  background(255);
  noLoop();
  for (int i=0; i<mybox.length; i++){
    mybox[i].display();
  }  
}

/*newBox = bounds you are trying to draw,
oldBox = bounds you are comparing to in your array*/
boolean CheckOverlap(Box newBox , Box oldBox) {
  if(newBox.posX > oldBox.posX && newBox.posX + newBox.Size < oldBox.posX + oldBox.Size/*It's almost 2, I doubt my logic is anywhere near ok. just compare the X values for overlap.*/){
     if(posY/*check if Y positions overlap*/){
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
  
  return false; 
}

class Box{
  float posX, posY;
  int Size;
  
  Box(float boxposX, float boxposY){
    posX=boxposX;
    posY=boxposY;
    Size = RandomiseSize();
  }
  
  int RandomiseSize() {
    int[] Sizes = {20,40,80};
    int Size = int(random(0,3));
    return Sizes[Size];
  }
  
  void display(){
    strokeWeight(1);
    rect(posX, posY, Size, Size);
  }
}