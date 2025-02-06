
#include <Servo.h>

Servo organic;  
Servo recyclable;
Servo disposable;

#define MINPOS 50         // 0 degree
#define MAXPOS 175        // 180 degree
#define DROP_WAIT 10000   // 10 second wait


int pos = 175;             

void setup() {
  organic.attach(9);  
  organic.write(pos); 
  recyclable.attach(10);  
  recyclable.write(pos); 
  disposable.attach(11);  
  disposable.write(pos); 

  delay(1000);
  Serial.begin(9600);
  Serial.println("Servo Motors are ready and set to pos.."+String(pos));
  delay(5000);
  Serial.println("Ready for Oprations...");
}

void loop() {
  if (Serial.available() > 0) {
    char data = Serial.read();
    
    Serial.print("Received Data: ");  
    Serial.println(data);

    if (data == 'o') {
      Serial.println("Organic bin in openration...");
      open_and_close_organic();
    } 
    else if (data == 'r') {
      Serial.println("Recyclable bin in openration...");
      open_and_close_recyclable();
    } 
    else if (data == 'd') {
      Serial.println("Disposable bin in openration...");
      open_and_close_disposable();
    }
    else if (data == 'x') {
      Serial.println("All bins are in openrations...");
      override();
    }
  }

  int sensorValue = analogRead(A1);
  if (sensorValue >= 1022){
      Serial.println("Running Manual Override...");
      override();
  }
}

void override(){
  Serial.println("Opening Bin...");
  for (pos = MAXPOS; pos >= MINPOS; pos -= 1) { // open
    organic.write(pos);   
    recyclable.write(pos);    
    disposable.write(pos);          
    delay(30);                       
  }
  delay(DROP_WAIT);
  Serial.println("Closing Bin...");
  for (pos = MINPOS; pos <= MAXPOS; pos += 1) { // close
    organic.write(pos);       
    recyclable.write(pos);    
    disposable.write(pos);         
    delay(30);                       
  }
}

void open_and_close_organic(){
  Serial.println("Opening Bin...");
  for (pos = MAXPOS; pos >= MINPOS; pos -= 1) { // open
    organic.write(pos);             
    delay(25);                       
  }
  delay(DROP_WAIT);
  Serial.println("Closing Bin...");
  for (pos = MINPOS; pos <= MAXPOS; pos += 1) { // close
    organic.write(pos);              
    delay(25);                       
  }
}

void open_and_close_recyclable(){
  Serial.println("Opening Bin...");
  for (pos = MAXPOS; pos >= MINPOS; pos -= 1) { // open
    recyclable.write(pos);             
    delay(25);                       
  }
  delay(DROP_WAIT);
  Serial.println("Closing Bin...");
  for (pos = MINPOS; pos <= MAXPOS; pos += 1) { // close
    recyclable.write(pos);              
    delay(25);                       
  }
}

void open_and_close_disposable(){
  Serial.println("Opening Bin...");
  for (pos = MAXPOS; pos >= MINPOS; pos -= 1) { // open
    disposable.write(pos);             
    delay(25);                       
  }
  delay(DROP_WAIT);
  Serial.println("Closing Bin...");
  for (pos = MINPOS; pos <= MAXPOS; pos += 1) { // close
    disposable.write(pos);              
    delay(25);                       
  }
}
