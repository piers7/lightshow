// Totally based on Adafruit's strand test sketch 
#include <Adafruit_NeoPixel.h>

#define PIN 6
#define PIXEL_COUNT 120

// Parameter 1 = number of pixels in strip
// Parameter 2 = Arduino pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(PIXEL_COUNT, PIN, NEO_GRB + NEO_KHZ800);

// IMPORTANT: To reduce NeoPixel burnout risk, add 1000 uF capacitor across
// pixel power leads, add 300 - 500 Ohm resistor on first pixel's data input
// and minimize distance between Arduino and first pixel.  Avoid connecting
// on a live circuit...if you must, connect GND first.

//struct Pixel {
//  int pos;
//  uint32_t color;
//  int decay;
//};
//
//const int LIVE_COUNT = 10;
//Pixel live[LIVE_COUNT];

// Setup the color sequence for the theatre chase
uint32_t colors[] = {
  strip.Color(127,   0,   0)  // red
  ,strip.Color(127, 127, 127)  // white
  ,strip.Color(  0,   0, 127)  // blue
  ,strip.Color(127, 127, 127)  // white
  ,strip.Color(  0,   127, 0)  // green
  ,strip.Color(127, 127, 127)  // white
  ,strip.Color(  0x55,   0x1A, 0x8B)  // purple
};
const int NUMBER_OF_COLORS = sizeof colors / sizeof colors[0];
  
//Pixel createRandomPixel(){
//    int pos = random(PIXEL_COUNT);
//    uint32_t col = Wheel(byte(random(PIXEL_COUNT)));
//    int decay = random(50);
//    return { pos, col, decay } ;
//}

void setup() {
  // set pin 0 to ground
  digitalWrite(0,0);
  
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
  
  // initialize my sparkly pixels
//  live = new Pixel[LIVE_COUNT];
//  for (int i=0;i<LIVE_COUNT;i++){
//    int pos = random(PIXEL_COUNT);
//    uint32_t col = Wheel(byte(random(PIXEL_COUNT)));
//    int decay = random(50);
//    live[i] = createRandomPixel();
//  }
}

void loop() {
//  runSparkles();
//  strip.show();
  // delay(100);

  rainbow(20);
  
  int i;
  for(int c=0; c < NUMBER_OF_COLORS; c++){
    // cycle through the color sequence as above
    for(i=0; i<10; i++)
      theaterChase(colors[c], 50); // White
    
    uint32_t nextColor = colors[(c+1) % NUMBER_OF_COLORS];
    colorWipe(nextColor, 5);
  }

// Send a theater pixel chase in...

//  colorWipe(strip.Color(255, 0, 0), 50); // Red
//  colorWipe(strip.Color(0, 255, 0), 50); // Green
//  colorWipe(strip.Color(0, 0, 255), 50); // Blue

//  glow(50);
  //rainbow(20);
  //rainbowCycle(20);
  //theaterChaseRainbow(50);
}

//void runSparkles(){
//  for(int i=0; i< sizeof(live); i++){
//    Pixel current = live[i];
//    current.decay--;
//    if(current.decay > 0){
//      strip.setPixelColor(current.pos, current.color);
//      strip.setBrightness((255*current.decay/10));
//      live[i] = current;
//    }else{
//      // TODO: what was supposed to happen here?
//      // live[i] = initPixel(); 
//    }
//  }  
//}

// Fill the dots one after the other with a color
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, c);
      strip.show();
      delay(wait);
  }
}

void glow(byte wait){
   for(byte i=0;i<255;i++){
    byte color = Wheel(i);
   for(byte p=0; p<strip.numPixels();p++){
    strip.setPixelColor(i,color);
   } 
   strip.show();
   delay(wait);
  }
}

void rainbow(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel((i+j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

// Slightly different, this makes the rainbow equally distributed throughout
void rainbowCycle(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256*5; j++) { // 5 cycles of all colors on wheel
    for(i=0; i< strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

//Theatre-style crawling lights.
void theaterChase(uint32_t c, uint8_t wait) {
  for (int j=0; j<10; j++) {  //do 10 cycles of chasing
    for (int q=0; q < 3; q++) {
      for (int i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, c);    //turn every third pixel on
      }
      strip.show();
     
      delay(wait);
     
      for (int i=0; i < strip.numPixels(); i=i+3) {
        strip.setPixelColor(i+q, 0);        //turn every third pixel off
      }
    }
  }
}

//Theatre-style crawling lights with rainbow effect
void theaterChaseRainbow(uint8_t wait) {
  for (int j=0; j < 256; j++) {     // cycle all 256 colors in the wheel
    for (int q=0; q < 3; q++) {
        for (int i=0; i < strip.numPixels(); i=i+3) {
          strip.setPixelColor(i+q, Wheel( (i+j) % 255));    //turn every third pixel on
        }
        strip.show();
       
        delay(wait);
       
        for (int i=0; i < strip.numPixels(); i=i+3) {
          strip.setPixelColor(i+q, 0);        //turn every third pixel off
        }
    }
  }
}

// Input a value 0 to 255 to get a color value.
// The colours are a transition r - g - b - back to r.
uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
   return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else if(WheelPos < 170) {
    WheelPos -= 85;
   return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  } else {
   WheelPos -= 170;
   return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  }
}

