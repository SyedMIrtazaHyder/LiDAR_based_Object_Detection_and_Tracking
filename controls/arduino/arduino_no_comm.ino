#include <ESP32Servo.h>

const int motorPin = 23;  // PWM pin connected to motor
int motorSpeed = 0;       // Variable to store motor speed (0-255)

// Define LEDC parameters
const int freq = 5000;    // Frequency (Hz)
const int resolution = 8; // Resolution (8 bits = 0-255)

void setup() {
  // Configure and attach the LEDC PWM channel to the specified GPIO pin
  ledcAttach(motorPin, freq, resolution);
}

void loop() {
  // Increase motor speed from 0 to 255
  for (motorSpeed = 0; motorSpeed <= 255; motorSpeed++) {
    ledcWrite(motorPin, motorSpeed);  // Write PWM signal to motor
    delay(20);  // Wait for 20 milliseconds
  }

  // Decrease motor speed from 255 to 0
  for (motorSpeed = 255; motorSpeed >= 0; motorSpeed--) {
    ledcWrite(motorPin, motorSpeed);  // Write PWM signal to motor
    delay(20);  // Wait for 20 milliseconds
  }
}
