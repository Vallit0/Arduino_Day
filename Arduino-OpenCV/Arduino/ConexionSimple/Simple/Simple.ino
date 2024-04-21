#include <Servo.h>

Servo servo1; 
Servo servo2;  

void setup() {
  servo1.attach(9);  
  servo2.attach(10); 
  servo2.write(90);
  delay(10);
  servo2.write(0);

  Serial.begin(9600); 
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); 
    switch (command) {
      case 'A':
        servo1.write(45); 
        break;
      case 'B':
        servo1.write(135); 
        break;
      case 'C':
        servo2.write(0); 
        break;
      case 'D':
        servo2.write(180); 
        break;
    }
  }
}
