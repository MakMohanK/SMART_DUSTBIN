// Author
// Mohan Kshirsagar


#include <Servo.h>

Servo organic;  
Servo recyclable;
Servo disposable;

#define MINPOS 0         // 0 degree
#define MAXPOS 180       // 180 degree
#define DROP_WAIT 10000  // 10 SEC


int pos = 0;             

void setup() {
  organic.attach(9);  
  organic.write(pos); 
  recyclable.attach(10);  
  recyclable.write(pos); 
  disposable.attach(11);  
  disposable.write(pos); 

  Serial.begin(9600);
  Serial.println("Servo Motors are ready and set to pos 0....");

  delay(5000);
}

void loop() {
  if (Serial.available() > 0) {
    char data = Serial.read();
    
    Serial.print("Received Data: ");  
    Serial.println(data);

    if (data == 'o') {
      Serial.println("Organic bin Opening and Closing");
      open_and_close_organic();
    } 
    else if (data == 'r') {
      Serial.println("Recyclable bin Opening and Closing");
      open_and_close_recyclable();
    } 
    else if (data == 'd') {
      Serial.println("Disposable bin Opening and Closing");
      open_and_close_disposable();
    }
    else if (data == 'x') {
      Serial.println("all bins Opening and Closing");
      override();
    }
  }

  int sensorValue = analogRead(A1);
  if (sensorValue >= 1022){
      Serial.println("Running Override .. "+String(sensorValue));
      override();
  }
}

void override(){
  for (pos = MINPOS; pos <= MAXPOS; pos += 1) { // open
    organic.write(pos);   
    recyclable.write(pos);    
    disposable.write(pos);          
    delay(30);                       
  }
  delay(DROP_WAIT);
  for (pos = MAXPOS; pos >= MINPOS; pos -= 1) { // close
    organic.write(pos);       
    recyclable.write(pos);    
    disposable.write(pos);         
    delay(30);                       
  }
}

void open_and_close_organic(){
  for (pos = MINPOS; pos <= MAXPOS; pos += 1) { // open
    organic.write(pos);             
    delay(25);                       
  }
  delay(DROP_WAIT);
  for (pos = MAXPOS; pos >= MINPOS; pos -= 1) { // close
    organic.write(pos);              
    delay(25);                       
  }
}

void open_and_close_recyclable(){
  for (pos = MINPOS; pos <= MAXPOS; pos += 1) { // open
    recyclable.write(pos);             
    delay(25);                       
  }
  delay(DROP_WAIT);
  for (pos = MAXPOS; pos >= MINPOS; pos -= 1) { // close
    recyclable.write(pos);              
    delay(25);                       
  }
}

void open_and_close_disposable(){
  for (pos = MINPOS; pos <= MAXPOS; pos += 1) { // open
    disposable.write(pos);             
    delay(25);                       
  }
  delay(DROP_WAIT);
  for (pos = MAXPOS; pos >= MINPOS; pos -= 1) { // close
    disposable.write(pos);              
    delay(25);                       
  }
}
