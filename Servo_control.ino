
//#include <Servo.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SERVOMIN  250 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  470 // this is the 'maximum' pulse length count (out of 4096)
//====KEY FOR ARRAY INDEXING=========
/*
0 - thumb
1 - thumb base
2 - index
3 - index middle phalanx
4 - middle
5 - ring and pinky
*/
//===================================

//==============================FINGER SETUP=========================================
//Servo thumb;
//Servo index;
//Servo middle;
//Servo ring;
byte servoPins[] = {2,4,5,1,0};
byte servoMin[] = {250, 250, 250, 160, 250};
byte servoMax = 470;
byte thumbmin = 290;
byte thumbmax = 150;
float servoPos[] = {250, 250, 250, 160, 250};
float newServoPos[] = {250, 250, 250, 160, 250};
float difference[] = {0, 0, 0, 0, 0}; //difference in old and new servo position
float servoFraction[] = {0.0, 0.0, 0.0, 0.0 ,0.0}; // fraction of servo range to move
//===================================================================================

//======PYTHON TO ARDUINO COMMUNICATION======
const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;
char messageFromPC[buffSize] = {0};
int newFlashInterval = 0;
//============================================

//=====TIME=======
unsigned long curMillis;
unsigned long prevReplyToPCmillis = 0;
unsigned long replyToPCinterval = 1000;
//================


//===============================================================
void setup() {
  Serial.begin(115200);
 
  // initialize the servo
  //index.attach(servoPins[0],800, 2150);
  //ring.attach(servoPins[1], 800, 2150);
  pwm.begin();
  

  
  // tell the PC Arduino is ready
  Serial.println("<Arduino is ready>");
  delay(500);
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates

  moveServo();
}
//==============================================================
void loop() {
//  curMillis = millis();
  getDataFromPC();
//  updateFlashInterval();
  updateServoPos();
  replyToPC();
//  flashLEDs();
  moveServo();
}
//==============================================================
void getDataFromPC() {

    // receive data from PC and save it into inputBuffer
    
  if(Serial.available() > 0) {

    char x = Serial.read();

      // the order of these IF clauses is significant
      
    if (x == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }
    
    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker) { 
      bytesRecvd = 0; 
      readInProgress = true;
    }
  }
}
//================================================================
void parseData() {

    // split the data into its parts
    
  char * strtokIndx; // this is used by strtok() as an index
  
  strtokIndx = strtok(inputBuffer,",");      // get the first part - the string
  strcpy(messageFromPC, strtokIndx); // copy it to messageFromPC

  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  servoFraction[0] = atof(strtokIndx);     // convert this part to an integer
  
  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  servoFraction[1] = atof(strtokIndx);     // convert this part to an integer
  
  strtokIndx = strtok(NULL, ","); 
  servoFraction[2] = atof(strtokIndx);     // convert this part to a float

  strtokIndx = strtok(NULL, ","); 
  servoFraction[3] = atof(strtokIndx);     // convert this part to a float

  strtokIndx = strtok(NULL, ","); 
  servoFraction[4] = atof(strtokIndx);

  
  Serial.print(servoFraction[0]);
}
//=================================================================
void replyToPC() {

  if (newDataFromPC) {
    newDataFromPC = false;
    Serial.print("<Msg ");
    Serial.print(messageFromPC);
    Serial.print(" NewFlash ");
    Serial.print(newFlashInterval);
    Serial.print(" SrvFrac ");
    Serial.print(servoFraction[0]);
    Serial.print(" SrvPos ");
    Serial.print(newServoPos[0]);
    Serial.print(" Time ");
    Serial.print(curMillis >> 9); // divide by 512 is approx = half-seconds
    Serial.println(">");
  }
}
//============================================================================
void updateServoPos() {

  byte servoRange[] = {220, 220, 220, 130, 220}; 
  for(int i = 0; i<=4; i++){
    if (servoFraction[i] >= 0 && servoFraction[i] <= 1) {
      newServoPos[i] = servoMin[i] + ( servoRange[i] * servoFraction[i]);
    
      //delay(1);
    }
  }
   
}
//============================================================================
void moveServo() {
  for(int i = 0; i<=4; i++){
      difference[i] = abs(servoPos[i] - newServoPos[i]);
      if (difference[i]>=2) {
        servoPos[i] = newServoPos[i];
        pwm.setPWM(servoPins[i], 0, servoPos[i]);
        //delay(1);
       }

  }


 // pwm.setPWM(2, 0, servoPos[0]);
  //pwm.setPWM(4, 0, servoPos[1]);
 //pwm.setPWM(5, 0, servoPos[2]);
  //pwm.setPWM(1, 0, servoPos[3]);
  //pwm.setPWM(0, 0, servoPos[4]);
  //Serial.println(servoPos[4]);
 

}

//==============================================================================
