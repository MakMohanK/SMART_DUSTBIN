// only tilt mechanism

#include <Servo.h>

Servo myservo;  

const int MIN_ANGLE = 70;
const int MID_ANGLE = 92;
const int MAX_ANGLE = 125;

void setup() {
  Serial.begin(9600);
  Serial.println("Ready for Oprations...");
  myservo.attach(9);  // attaches the servo on pin 9 to the Servo object
  myservo.write(MID_ANGLE);   
  delay(1000);
}

void loop() {
  if (Serial.available()){
    char data = Serial.read();
    Serial.println(data);
    if (data == 'o'){
      organic_found();
    }
    else if (data == 'r'){
      recycle_found();
    }
  }
}

void organic_found(){
  Serial.println("Opening Organic Bin...");
  for (int i = 1; i <= 3; i++){
    myservo.write(MAX_ANGLE); 
    delay(i*1000);
    myservo.write(MID_ANGLE);
    delay(1000);
  }
  Serial.println("Closing Organic Bin...");
}

void recycle_found(){
  Serial.println("Opening Recycle Bin...");
  for (int i = 1; i <= 3; i++){
    myservo.write(MIN_ANGLE); 
    delay(i*1000);
    myservo.write(MID_ANGLE);
    delay(1000);
  }
  Serial.println("Closing Organic Bin...");
}