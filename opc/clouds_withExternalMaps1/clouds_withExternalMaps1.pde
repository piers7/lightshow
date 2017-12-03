OPC opc1;
OPC opc2;
float dx, dy;

void setup()
{
  size(300, 200);

  opc1 = setupDropWall("pizero1.local");
  // opc2 = setupBackVeranda("pizero3.local");
  
  colorMode(HSB, 100);
}

OPC setupDropWall(String address){
  // Connect to the local instance of fcserver. You can change this line to connect to another computer's fcserver
  OPC opc = new OPC(this, address , 7890);

  float spacingX = width / (4 * 4);
  float spacing = height / 20.0;
  //   void ledGrid(int index, int stripLength, int numStrips, float x, float y, float ledSpacing, float stripSpacing, float angle, boolean zigzag)

  // starting offset of 50,100 is because each block has 48px + 2px unused
  opc.ledGrid(0, 4, 12, width/4, height/2, spacingX, spacing, 0, true);
  opc.ledGrid(50, 4, 12, 2 * width/4, height/2, spacingX, spacing, 0, true);
  opc.ledGrid(100, 4, 12, 3 * width/4, height/2, spacingX, spacing, 0, true);

  // Put two more 8x8 grids to the left and to the right of that one.
  //opc.ledGrid8x8(64, width/2 - spacing * 8, height/2, spacing, 0, true);
  //opc.ledGrid8x8(128, width/2 + spacing * 8, height/2, spacing, 0, true);
  
  // Make the status LED quiet
  opc.setStatusLed(false);
  return opc;
}

OPC setupBackVeranda(String address){
  OPC opc = new OPC(this, address, 7890);

  int rows = 60;
  int cols = 7;
  //   void ledGrid(int index, int stripLength, int numStrips, float x, float y, float ledSpacing, float stripSpacing, float angle, boolean zigzag)

  opc.ledGrid(0, rows, cols, width/2, height/2, height/(float)rows, width/(float)cols, PI/2, true);
  return opc;
}

float noiseScale=0.02;

float fractalNoise(float x, float y, float z) {
  float r = 0;
  float amp = 1.0;
  for (int octave = 0; octave < 4; octave++) {
    r += noise(x, y, z) * amp;
    amp /= 2;
    x *= 2;
    y *= 2;
    z *= 2;
  }
  return r;
}

void draw() {
  long now = millis();
  float speed = 0.002;
  float angle = sin(now * 0.001);
  float z = now * 0.00008;
  float hue = now * 0.01;
  float scale = 0.005;

  dx += cos(angle) * speed;
  dy += sin(angle) * speed;

  loadPixels();
  for (int x=0; x < width; x++) {
    for (int y=0; y < height; y++) {
     
      float n = fractalNoise(dx + x*scale, dy + y*scale, z) - 0.75;
      float m = fractalNoise(dx + x*scale, dy + y*scale, z + 10.0) - 0.75;

      color c = color(
         (hue + 80.0 * m) % 100.0,
         100 - 100 * constrain(pow(3.0 * n, 3.5), 0, 0.9),
         100 * constrain(pow(3.0 * n, 1.5), 0, 0.9)
         );
      
      pixels[x + width*y] = c;
    }
  }
  updatePixels();
}