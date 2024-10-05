#include <Arduino.h>
#include <Servo.h>

Servo motor;  // Create a Servo object

void setup() {
  Serial.begin(115200);  // Start serial communication
  motor.attach(9);       // Attach the servo to pin 9
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    if (command == "left") {
      motor.write(45);  // Move servo to the left (45 degrees)
    } else if (command == "right") {
      motor.write(135);  // Move servo to the right (135 degrees)
    }
  }
}
