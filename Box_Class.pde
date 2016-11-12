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