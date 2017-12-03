String message = "HAPPY CHRISTMAS"; 
float messageWidth;
int initialPosition;
int position;
OPC opc;
int rows = 4;
int cols = 4*6;

void setup() {
  size(180, 80);
  //textSize(height);
  PFont font = createFont("Verdana Bold", height);
  textFont(font);
  messageWidth = textWidth(message) + 10;
  initialPosition = width;
  position = initialPosition;

  //Object[] fontList = PFont.list();
  //println(fontList);

  // Connect to the local instance of fcserver
  opc = new OPC(this, "localhost", 7890);
  // ledGrid wants to build long strips, horizontally, then add rows
  // so because I've wired up the other way, need to rotate (half-pi)
  // effect is to flip the y axis, hence negative spacing
  // void ledGrid(int index, int stripLength, int numStrips, float x, float y,
  //            float ledSpacing, float stripSpacing, float angle, boolean zigzag)
  opc.ledGrid(0, rows, cols, width/2, height/2, height/rows * .7, -6, HALF_PI, false);
}

void draw() {
  background(0);
  textSize(height);
  text(message, position, height - 10);
  position--;
  if(position < -messageWidth)
    position = initialPosition;
}