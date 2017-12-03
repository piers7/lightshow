String message = "HAPPY CHRISTMAS"; 
float messageWidth;
int initialPosition;
int position;
OPC opc;
int rows = 4;
int cols = 4*6;

void setup() {
  size(180, 80);

  // Connect to OPC server
  //opc = new OPC(this, "localhost", 7890);
  //opc.ledGrid(0, rows, cols, width/2, height/2, height/rows * .7, -6, HALF_PI, false);
}

int offset = 0;
void draw() {
  background(0);
  strokeWeight(10);
  offset = (offset + 1) % 20;
  for(int i = -20 + offset;i<width;i+=5){
    if(i%2==0)
      stroke(255,0,0);
    else
      stroke(0,255,0);

    int x = i*5;
    line(x,0,x+height/2,height/2);
    line(x,height,x+height/2,height/2);
  }
  delay(100);
}