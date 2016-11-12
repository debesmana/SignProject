Box[] mybox= new Box[50];

void setup(){
  size(500,500);
  for (int i=0; i<mybox.length; i++){
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
    rectMode(CENTER);
    rect(posX, posY, Size, Size);
  }
  
  void GetBounds(){
    
  }
}