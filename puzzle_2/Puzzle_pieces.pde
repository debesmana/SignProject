class PuzzlePieces{
  float posX, posY;
  int size;
  
  PuzzlePieces(float puzzlePosX, float puzzlePosY){
    posX= puzzlePosX;
    posY= puzzlePosY;
    size= RandomSize();
  }
  
  int RandomSize(){
    int[] Sizes= {10};
    int random= 0;
    return Sizes[random];
  }
  
  void display(){
    strokeWeight(1);
    rect(posX, posY, size, size);
  }
}